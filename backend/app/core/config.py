from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "disc_loan_db"

    class Config:
        env_file = ".env"

settings = Settings()

# mongodb+srv://wonkyjaveriana2037_db_user:xWV3LupyQUm1QicK@cluster0.soxfim2.mongodb.net/?appName=Cluster0
#what is above is the connection string to connect to the MongoDB database hosted on MongoDB Atlas. It includes the username, password, and cluster information needed to establish a connection to the database.