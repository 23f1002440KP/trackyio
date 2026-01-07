from app import create_app 
from app.core.config import config
from app.db.extensions import db




app = create_app(config.app_name)

with app.app_context():
    db.create_all()


if __name__ == "__main__" :
    
    app.run(
        debug=config.debug,
        port=config.port
        )
 