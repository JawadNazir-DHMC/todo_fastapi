from starlette.config import  Config
from starlette.datastructures import Secret

try:
    config=Config(".env")
except FileNotFoundError:
    config=Config()

Data_Base_URL=config("Data_Base_URL",cast=Secret)
Test_Data_Base_URL=config("Test_Data_Base_URL",cast=Secret)
