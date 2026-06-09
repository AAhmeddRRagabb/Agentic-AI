# ------------------------------------------------------
# Alhamdulillah
# Error Handling Practice
# ------------------------------------------------------


class AppError(Exception):
    pass

class ProductNotFoundError(AppError):
    pass

class InvalidProductDataError(AppError):
    pass

class ProductStorageError(AppError):
    pass


PRODUCTS = {
    1: {
        'id'   : 1,
        "name" : "laptop",
        "price": 250
    },

    2: {
        'id'   : 2,
        "name" : 'mouse',
        'price': 10
    }
}


def get_product(product_id: int) -> dict:
    for product_index, product in PRODUCTS.items():
        if product_id == product["id"]:
            return PRODUCTS[product_index]
    
    raise ProductNotFoundError("Product not found error")

def validate_product(product: dict) -> None:
    if not product["name"] or product["price"] <= 0:
        raise InvalidProductDataError("Invaldi data")


import time
def save_product(product: dict, accepted_delay: int):
    if accepted_delay <= 3:
        max_product_index = max(list(PRODUCTS.keys()))

        PRODUCTS[max_product_index + 1] = product
    else:
        raise ConnectionError("Storage connection error")



def product_service(product_id: int, accepted_delay: int):
    product = get_product(product_id)
    validate_product(product)
  

    try:
        save_product(product, accepted_delay)
    except ConnectionError as e:
        raise ProductStorageError("could not save product") from e
    



def api_handler(product_id: int, accepted_delay: int) -> dict:
    try:
        product = product_service(product_id, accepted_delay)

        return {
            "status_code": 200,
            "data": product,
        }

    except ProductNotFoundError as e:
        return {
            "status_code": 404,
            "detail": str(e),
        }

    except InvalidProductDataError as e:
        return {
            "status_code": 400,
            "detail": str(e),
        }

    except ProductStorageError as e:
        return {
            "status_code": 503,
            "detail": str(e),
        }

    except Exception:
        return {
            "status_code": 500,
            "detail": "Internal server error",
        }
    
print(api_handler(1, 1))  
print(api_handler(99, 1)) 
print(api_handler(1, 5))