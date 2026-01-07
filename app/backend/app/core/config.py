from dotenv import load_dotenv
import os
from dataclasses import dataclass 
load_dotenv()

class Config():
    db_name : str = os.getenv("DATABASE_NAME")
    port : str  = os.getenv("PORT")
    
    SQLALCHEMY_DATABASE_URI  = f"sqlite:///{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    BCRYPT_LOG_ROUNDS = 12    


@dataclass
class LocalDevConfig(Config):
    app_name : str = "Tracky.io // Dev"
    debug : bool = True
    
    log_file : str = "app/logs/dev_logs.log"
    


@dataclass
class ProdConfig(Config):
    app_name : str = "Tracky.io // Prod"
    debug : bool = False
    
    log_file : str = "app/logs/prod_logs.log"
    

ENV : str = os.getenv("ENV")


if ENV.lower() == 'local' :
    config = LocalDevConfig()
else : 
    config = ProdConfig()