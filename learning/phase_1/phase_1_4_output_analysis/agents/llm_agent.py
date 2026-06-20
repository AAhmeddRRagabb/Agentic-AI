from typing   import Any
from pydantic import BaseModel, ValidationError

from io import TextIOWrapper
import json

from helpers.functional import log_message
from helpers.settings import DB_TABLES_EXIST, DB_ALLOWED_QUERY_TYPES, SENSITIVE_KEYWORDS

import groq
from llms_core.groq import GroqLLMClient
from llms_core.groq.config import PROVIDER_GROQ


class LLMAgent:
    """
    Class for abstracting the Agent workflow:
        - pre-processing data [if required]
        - calling the model
        - post-processing model output [if required]
        - validate the output

    Args:
        model_provider  : str
        provider_api_key: str
        model_name      : str
        system_prompt   : str
        response_format : dict[str, Any]
        output_schema   : BaseModel
        **kwargs        : dict[str, Any]
    """
    def __init__(
        self,
        model_provider  : str,
        provider_api_key: str,
        model_name      : str,
        system_prompt   : str,
        response_format : dict[str, Any],
        output_schema   : type[BaseModel],
        log_file        : TextIOWrapper,
        **kwargs        
    ):
        # init
        self.model_provider   = model_provider
        self.model_name       = model_name
        self.system_prompt    = system_prompt
        self.response_format  = response_format
        self.output_schema    = output_schema  
        self.log_file         = log_file
        self.kwargs           = kwargs

        self.llm_client = self.get_llm_client(provider_api_key)
    

    def get_llm_client(self, api_key: str) -> GroqLLMClient:
        if self.model_provider == PROVIDER_GROQ:
            return GroqLLMClient(api_key = api_key)
        
        raise ValueError(f"Unsupported model provider: {self.model_provider}")
    
    # ------------ Invoking -------------------#
    def invoke(self, query: str) -> str:
        return self.llm_client.generate(
            model_name      = self.model_name,
            query           = query,
            system_prompt   = self.system_prompt,
            response_format = self.response_format,
            **self.kwargs
        )
    # ------------ Post-processing ---------- #
    def parse_model_response(self, model_response: str | dict[str, Any]) -> dict[str, Any]:
        if isinstance(model_response, str):
            model_response = json.loads(model_response)

        validated_output = self.output_schema.model_validate(model_response)

        return validated_output.model_dump()


    # ------------ validation ---------- #
    def validate_schema(self, model_response: str | dict[str, Any]) -> dict[str, Any]:
        """
        Validate that the model correctly produced the required schema
        """
        try:
            parsed_model_response = self.parse_model_response(model_response)
            return parsed_model_response
        
        except (ValidationError, json.JSONDecodeError):
            raise


    def validate_semantic(self, model_response_dict: dict[str, Any]) -> bool | dict[str, str | bool]:
        """
        Validate logical rules:
            >> query = None ---> used_tables = None
            >> query != None --> used_tables from existing tables
            >> query starts with the query type
        """
        sql_query = model_response_dict.get("query")
        tables_used = model_response_dict.get("tables_used")
        query_type = model_response_dict.get("required_query_type")

        # None query
        if sql_query is None:
            if tables_used is None or len(tables_used) == 0:
                return True
            
            tables_used_str = ", ".join(tables_used)
            return {
                "problem": (
                    "When the SQL query is None, used tables should also be None, but you have violated this rule.\n"
                    "Your response:\n"
                    f">> SQL Query: {sql_query}\n"
                    f">> Tables Used: {tables_used_str}"
                )
            }
            
        if tables_used is None or len(tables_used) == 0:
            return {
                "problem": (
                    "When the SQL query is None, used tables should also be None, but you have violated this rule.\n"
                    "Your response:\n"
                    f">> SQL Query: {sql_query}\n"
                    f">> Tables Used: None"
                )
            }

        # not None query
        if not set(tables_used).issubset(DB_TABLES_EXIST):  
            db_tables_str = ", ".join(DB_TABLES_EXIST)
            used_tables_str = ", ".join(tables_used)
            return {
                "problem": (
                    "You used tables not found in the database.\n"
                    f">> You used ({used_tables_str})\n"
                    f">> >> Database contains ({db_tables_str})"
                )
            }


        # query type & query
        if not sql_query.lower().startswith(query_type.lower()):
            return {
                "problem"  : (
                    "You provided a query that does not start with the query type.\n"
                    f">> Query Type: {query_type}\n"
                    f">> SQL Query: {sql_query}"
                )
            }
        
        return True



    def validate_business_rules(self, model_response_dict: dict[str, Any], user_query: str) -> bool | dict[str, Any]:
        """
        Validate:
            >> If non SELECT query --> SQL query & tables should be None
            >> If users asked about sensitive data -----> Query | tables should be None
        """
        sql_query = model_response_dict.get("query")
        required_query_type = model_response_dict.get("required_query_type")
        tables_used = model_response_dict.get("tables_used")

        # not allowed query types
        if required_query_type.lower() not in DB_ALLOWED_QUERY_TYPES:
            if sql_query is not None:
                return {
                    "problem"  : (
                        f"For not allowed query type ({required_query_type}), query & tables used should be None.\n"
                        "Your Response:\n"
                        f">> Required Query Type: {required_query_type}\n"
                        f">> Sql Query: {sql_query}\n"
                        f">> Tables Used: {tables_used}"
                    )
                }
            
        
        # sensitive data
        for sensitive_keyword in SENSITIVE_KEYWORDS:
            if sensitive_keyword in user_query.lower().strip():
                if sql_query is not None:
                    return {
                        "problem" : (
                            "There should be no SQL query response if the user asks for sensitive keywords / data (passwords, credits, etc.)."
                            f"\n>> User Query: {user_query}"
                            f"\n>> Your SQL Query: {sql_query}"
                        )
                    }


        return True


    def validate_model_response(self, model_response: str | dict[str, Any], user_query: str) -> dict[str, Any]:
        # schema
        try:
            model_response_dict = self.validate_schema(model_response)

        except (ValidationError, json.JSONDecodeError):
            raise


        # semantic
        semantic_validation_results = self.validate_semantic(model_response_dict)
        if semantic_validation_results is not True:
            return {
                "validated": False,
                "response" : None,
                "violation": "semantic_violation",
                "error"    : semantic_validation_results["problem"]
            }

        # business rules
        business_rules_validation_results = self.validate_business_rules(model_response_dict, user_query)
        if business_rules_validation_results is not True:
            return {
                "validated": False,
                "response" : None,
                "violation": "business_rules_violation",
                "error"    : business_rules_validation_results["problem"]
            }


        # validated
        return {
            "validated": True,
            "response" : model_response_dict,
            "violation" : None,
            "error"    : None
        }

    # ----------------- The Whole Pipeline ---------------------- #
    def __call__(self, query: str, round_number: int = 1, max_retries: int = 3) -> dict[str, Any]:
        log_message(self.log_file, f"\t>> Round {round_number}")
        
        # invoke
        try:
            model_response = self.invoke(query = query)
            validated_model_response = self.validate_model_response(model_response, query)
            
        except (ValidationError, json.JSONDecodeError, groq.BadRequestError):
            validated_model_response = {
                "validated": False,
                "error"    : "You have not generated a valid schema. Only respond with the required schema if available or with a JSON object if specified.",
                'violation' : "bad_response",
                "response" : None
            }

            
            

        if validated_model_response["validated"]:
            return {
                "validated": True,
                "sql_query": validated_model_response["response"]["query"],
                "required_query_type": validated_model_response["response"]["required_query_type"],
                "tables_used": validated_model_response["response"]["tables_used"]
            }
        
        if round_number > max_retries:
            return validated_model_response
        

        # self-correction
        self_correction_query = self.get_self_correction_query(validated_model_response, query)
        return self(
            query          = self_correction_query, 
            round_number   = round_number + 1,  
            max_retries    = max_retries
        )

        
    def get_self_correction_query(self, not_validated_output: dict[str, Any], query: str) -> str:
        error = not_validated_output["error"]
        violation = not_validated_output["violation"]

        query = (
            "You have failed in the previous user natural language query.\n"
            f"Error type you produced: {violation}\n"
            f"Exact Problem: {error}\n"
            f"Correct your response, Here is the user natural language query again: {query}\n"
        )

        return query

            





            

            

            
