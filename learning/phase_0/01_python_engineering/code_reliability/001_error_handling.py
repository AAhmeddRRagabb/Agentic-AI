# ------------------------------------------------------
# Alhamdulillah
# Error Handling
# ------------------------------------------------------


## Task 1: Do not use Exception always

def parse_age(age: str) -> int:
    return int(age)

def read_file(file_path: str) -> str:
    with open(file_path, mode = "r", encoding = 'utf-8') as f:
        return f.read()

def parse_age_raise(age: str) -> int:
    try:
        return int(age)
    except ValueError:
        raise


class FileProcessingError(Exception):
    pass



# custom errors
class AppError(Exception):
    pass
class ProductNotFoundError(AppError):
    pass
class InvalidProductPriceError(AppError):
    pass


def get_product(product_id: int) -> dict:
    if int(product_id) == 1000:
        raise AppError("app error")
    if int(product_id) >= 50:
        raise ProductNotFoundError("product not found error")
    if int(product_id) <= 0:
        raise InvalidProductPriceError("product price error")
    
    return {
        "Product_id": product_id,
        "Content"   : "success"
    }

# low level --> high level application-related errors
class EmailSendingError(Exception):
    pass

import time
def send_email(delay) -> str:
    if delay < 5:
        time.sleep(delay)

        return {
            'success': True,
            "email"  : "Hi, Hamada"
        }

    raise ConnectionError





def app():
    pass

if __name__ == "__main__":
    print("============> Choose a Task <==============")

    print(">> 1. Parsing Age")
    print(">> 2. Reading File")
    print(">> 3. Parsing Age with Raise")
    print(">> 4. Exception Chaining")
    print(">> 5. Create Custom Exceptions")
    print(">> 6. Low level to high level exceptions")

    task = int(input("Enter task number: ").strip())

    if task == 1:
        age = input("=> Enter an age: ").strip()

        try:
            age = parse_age(age)
        except ValueError:
            print("Age is invalid")
        else:
            print(age)
    
    # ---------------------------------------------------------------
    elif task == 2:
        file_path = input("=> Enter File Path: ").strip()

        try:
            content = read_file(file_path)
        except FileNotFoundError:
            print("File not found")
        else:
            print(content)
    # ---------------------------------------------------------------
    elif task == 3:
        age = input("=> Enter an age: ").strip()
        try:
            parse_age_raise(age)
        except ValueError as e:
            print(e)
        else:
            print(age)
    # ---------------------------------------------------------------
    elif task == 4:
        file_path = input("=> Enter File Path: ").strip()

        try:
            content = read_file(file_path)
        except FileNotFoundError as e:
            raise FileProcessingError("File not found") from e
        else:
            print(content)
    # ---------------------------------------------------------------
    elif task == 5:
        product_id = input("=> Enter product id: ").strip()
        try:
            product = get_product(product_id)
        except ProductNotFoundError as e:
            print(e)
        except InvalidProductPriceError as e:
            print(e)
        except AppError as e:
            print(e)
        else:
            print(product)
        finally:
            print("goodbye")
    # ---------------------------------------------------------------
    elif task == 6:
        delay = int(input('=> Enter delay: ').strip())

        try:
            email = send_email(delay)
        except ConnectionError as e:
            raise EmailSendingError("Error") from e
        else:
            print(email)
        finally:
            print("goodbye")
    

    else:
        exit()
