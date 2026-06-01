# ------------------------------------------------------
# Alhamdulillah
# pydantic Models
# ------------------------------------------------------


# ----------------------------------- Pydantic Models -------------------------------------------------------
# >> The most-common data validation technique used nowadays (such in FastAPI, Agents, ...)
# >> Sections:
# -----> # 1.0 Basic Validation
# -----> # 2.0 Validation with Default values
# -----> # 3.0 Converting into dict / json
# -----> # 4.0 Exploring many fields types
# -----> # 5.0 Using `Annotated` for re-usable validation types
# -----> # 6.0 Using validation-friendly data types from Pydantic
# -----> # 7.0 Building Custom validation-friendly data types
# -----> # 8.0 Computed Field --> Field produced based on other fields
# -----> # 9.0 Creating Models
# -----> # 10.0 Config Dict

# >> Resource: https://www.youtube.com/watch?v=M81pfi64eeM&t=2359s
# ------------------------------------------------------------------------------------------------------------

from pydantic import BaseModel, Field

# Utilities
def print_title(title: str):
    print()
    print()
    title = " " + title + " "
    print(title.center(100, '='))


def print_error(error: str):
    print(f"\t>> Error     : {error}")
    print(f"\t>> Error Type: {type(error)}")


# 1.0 Basic Validation
class validator(BaseModel):
    name: str
    age : int

print_title("1.0 Basic Validation")
print(f"\t>> Validated    : {validator(name = "Ahmed", age = 30)}")
try:
    print(f"\t>> Not Validated: {validator(name = "Ahmed", age = "Mohammed")}")
except Exception as e:
    print_error(e)
# ------------------------------------------------------------------------------------------


# 2.0 Validation with Default values
class User(BaseModel):
    # required fields 
    user_id   : int
    user_name : str
    user_age  : int

    # optional
    is_active     : bool = False
    num_of_friends: int | None = None 

print_title("2.0 Validation with Default values")
user = User(user_id = 2, user_name = "Ahmed", user_age = 30)
print(f"\t>> User                                    : {user}")

user.num_of_friends = "50"
print(f"\t>> Re-assigning is not validated by default: {user}")
# ------------------------------------------------------------------------------------------


# 3.0 Converting into dict / json
user.num_of_friends = 50
print_title("3.0 Converting into dict / json")
print(f"\t>> Dict: {user.model_dump()}")
print(f"\t>> Json: {user.model_dump_json(indent = 2)}")
# ------------------------------------------------------------------------------------------

# 4.0 Exploring many fields types
from pydantic import Field
from typing import Literal
from datetime import datetime, UTC

class BlogPost(BaseModel):
    title  : str
    content: str
    
    view_count: int = 0
    is_published: bool = False

    comments  : list[str] = Field(default_factory = list)
    created_at: datetime  = Field(default_factory = lambda: datetime.now(tz = UTC))

print_title("4.0 Testing Various Instances")

post_1 = BlogPost(
    title = "My First Post",
    content = "This is the content of the blog post.",
)
print(f"\t>> Valid - required fields only: {post_1.model_dump_json(indent = 2)}")
print()

post_2 = BlogPost(
    title = "Python Engineering",
    content = "Learning Pydantic models.",
    view_count = 150,
    is_published = True,
    comments = ["Great post!", "Very useful."],
    created_at = datetime.now(tz = UTC),
)
print(f"\t>> Valid - all fields provided : {post_2.model_dump_json(indent = 2)}")
print()


post_3 = BlogPost(
    title = "Datetime Parsing",
    content = "Pydantic can parse ISO datetime strings.",
    created_at = "2026-05-30T10:00:00Z",
)
print(f"\t>> Valid: Pydantic can parse datetime string: {post_3.model_dump_json(indent = 2)}")
print()


print("\t>> Invalid: missing required field `title`")
try:
    post = BlogPost(
        content = "This post has no title.",
    )
    print(post)
except Exception as e:
    print_error(e)
print()

print("\t>> Invalid: missing required field `content`")
try:
    post = BlogPost(
        title = "Post Without Content",
    )
    print(post)
except Exception as e:
    print_error(e)
print()

print("\t>> Invalid: view_count should be int")
try:
    post = BlogPost(
        title = "Bad View Count",
        content = "view_count must be an integer.",
        view_count = "many",
    )
    print(post)
except Exception as e:
    print_error(e)
print()

print("\t>> Invalid: comments should be list[str]")
try:
    post = BlogPost(
        title = "Bad Comments",
        content = "comments must be a list of strings.",
        comments = "nice post",
    )
    print(post)
except Exception as e:
    print_error(e)
print()

print("\t>> Invalid: one comment is not str")
try:
    post = BlogPost(
        title = "Bad Comment Item",
        content = "Every comment must be a string.",
        comments = ["Good", 123, "Nice"],
    )
    print(post)
except Exception as e:
    print_error(e)
print()

print("\t>> Invalid: created_at should be valid datetime")
try:
    post = BlogPost(
        title = "Bad Date",
        content = "created_at must be a valid datetime.",
        created_at = "not-a-date",
    )
    print(post)
except Exception as e:
    print_error(e)
# ------------------------------------------------------------------------------------------

# 5.0 Using `Annotated` for re-usable validation types
from typing import Annotated

Name = Annotated[str, Field(min_length = 5, max_length = 20)]
Age  = Annotated[int, Field(ge = 10, le = 55)]
class User(BaseModel):
    name: Name
    age : Age

print_title("5.0 Using `Annotated` for re-usable validation types")
print(f"\t>> Valid: {User(name = "Ahmed Ragab", age = 20)}")

try:
    user = User(name = "ahm", age = 3)
except Exception as e:
    print_error(e)
# ------------------------------------------------------------------------------------------

# 6.0 Using validation-friendly data types from Pydantic
from uuid import UUID, uuid4
from typing import Annotated
from pydantic import Field, EmailStr, SecretStr, HttpUrl

class User(BaseModel):
    user_id: UUID = Field(default_factory = uuid4)
    user_name: Annotated[str, Field(min_length = 5, max_length = 20)]
    user_email: EmailStr
    user_passw: SecretStr
    website: HttpUrl | None = None

print_title("6.0 Using validation-friendly data types from Pydantic")
user = User(user_name = "Ahmed Ragab", user_email = "ahmed@gmail.com", user_passw = "ahmed@123")
print(f"\t>> Example: {user}")
print(f"\t>> Printing the True passwrod: {user.user_passw.get_secret_value()}")
# ------------------------------------------------------------------------------------------

# 7.0 Creating custom validation strategies

from pydantic import field_validator, model_validator

class User(BaseModel):
    user_id: UUID = Field(default_factory = uuid4)
    user_name: Annotated[str, Field(min_length = 5, max_length = 20)]
    user_email: EmailStr
    user_passw: SecretStr
    confirm_password: SecretStr
    website: HttpUrl | None = None

    # apply custom validation on user_name
    @field_validator('user_name', mode = "before")
    @classmethod
    def validate_username(cls, username: str) -> str:
        if not username.replace("_", "").isalnum():
            raise ValueError("Only underscode, letters, and numbers are valid in user_name")
        return username.lower()
    
    @field_validator("website", mode = "before") # applying the function (validator) before pydantic main validation strategies -> useful for adding some known modifications
    @classmethod
    def validate_website(cls, website: str | None) -> str:
        if website and not website.startswith(("http://", "https://")):
            return f"https://{website}"
        
        return website
    

    @model_validator(mode = "after") # applied on the whole model [many | all fields]
    def validate_password(self):
        if self.user_passw != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    

print_title("7.0 Creating custom validation strategies")
user = User(user_name = "Ahmed_Ragab", user_email = "ahmed@gmail.com", user_passw = "ahmed@123", confirm_password = "ahmed@123", website = "http://www.google.com")
print(f"\t>> Custom validation on user_name (valid): {user.model_dump_json(indent = 2)}")
print()

user = User(user_name = "Ahmed_Ragab", user_email = "ahmed@gmail.com", user_passw = "ahmed@123", confirm_password = "ahmed@123", website = "www.google.com")
print(f"\t>> Custom validation on website (valid): {user.model_dump_json(indent = 2)}")
print()


user = User(user_name = "Ahmed_Ragab", user_email = "ahmed@gmail.com", user_passw = "ahmed@123", confirm_password = "ahmed@123", website = "www.google.com")
print(f"\t>> Custom validation on password (valid): {user.model_dump_json(indent = 2)}")
print()

try:
    user = User(user_name = "Ahmed Ragab", user_email = "ahmed@gmail.com", user_passw = "ahmed@123", confirm_password = "ahmed@123")
except Exception as e:
    print_error(e)
print()

try:
    user = User(user_name = "Ahmed_Ragab", user_email = "ahmed@gmail.com", user_passw = "ahmed@123", confirm_password = "ahmed@456")
except Exception as e:
    print_error(e)
# ------------------------------------------------------------------------------------------

# 8.0 Computed Field --> Field produced based on other fields

from pydantic import EmailStr, computed_field, BaseModel

class User(BaseModel):
    email: EmailStr | None

    @computed_field
    @property
    def is_signed_up(self) -> bool:
        return self.email is not None

print_title("8.0 Computed Field --> Field produced based on other fields")
print(f"\t>> Computed Feild #1: {User(email = "ahmed@gmail.com").model_dump_json(indent = 2)}")
print(f"\t>> Computed Feild #2: {User(email = None).model_dump_json(indent = 2)}")
# ------------------------------------------------------------------------------------------

# 9.0 Creating Models

## basically
# class Model1(BaseModel):
#     data: str

## Nested Models
# class Model2(BaseModel):
#     data_list = list[Model1]

## from dict [dict should have the same keys as Model attbs]
# model_2_from_dict = Model2(**dict)
# or 
# model_2_from_dict = Model2.model_validate(dict)


## from json
# model_2_from_json = Model2.model_validate_json(json_file)
# ------------------------------------------------------------------------------------------

# 10.0 Config Dict

from pydantic import ConfigDict, BaseModel, Field
from uuid import UUID, uuid4

class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name = True,    # allow alises
        strict = True,              # no type casting -> use exact same types required
        extra = "allow",            # extra variables [allow - forbid "error" - ignore "accept but not presented"]
        validate_assignment = True, # validate on re-assignment an attb
        # frozen = True,            # instance created is frozen
    ) 

    uid: UUID = Field(default_factory = uuid4, alias = "id")
    name: str = Field(min_length = 5, max_length = 20, alias = "fname")
    passw: str

data = {
    "id": uuid4(),
    "fname": "Ahmed",
    "passw": "ahmed256"
} 

print_title("10.0 Config Dict")

user = User.model_validate(data)
# user = User(**data)

print(f"\t>> By real attb name        : {user.model_dump_json(indent = 2)}")
print(f"\t>> By alias attb name       : {user.model_dump_json(indent = 2, by_alias = True)}")
print(f"\t>> Excluding some attbs     : {user.model_dump_json(indent = 2, by_alias = True, exclude = {"passw"})}")
print(f"\t>> Inlcuding only some attbs: {user.model_dump_json(indent = 2, by_alias = True, include = {"uid", "name"})}")
print()
# re-assigning
try:
    user.name = 'ahm'
except Exception as e:
    print_error(e)

print()
print()