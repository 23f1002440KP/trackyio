from flask import Flask, jsonify , request, g
from app.core.logging import setup_logging
from app.core.config import config,Config
import time 
import uuid
from datetime import timedelta

from app.db.extensions import db, jwt

from app.blueprints.health_check import health_bp
from app.blueprints.auth import auth_bp
from app.blueprints.projects import projects_bp
from app.blueprints.tasks import tasks_bp
 
def create_app(name:str = "tracky.io") -> Flask:
    app = Flask(name)
    
    @app.before_request
    def start_request():
        g.start_time = time.time()
        g.request_id = request.headers.get(
            "X-Request-ID", str(uuid.uuid4())
        )

    @app.after_request
    def log_request(response):
        duration = round(time.time() - g.start_time, 4)

        app.logger.info(
            "req=%s %s %s -> %s (%ss)",
            g.request_id,
            request.method,
            request.path,
            response.status_code,
            duration
        )

        response.headers["X-Request-ID"] = g.request_id
        return response
    
    setup_logging(app)
    
    app.config.from_object(Config)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    
    db.init_app(app)
    jwt.init_app(app)
    


   
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    
    print(app.url_map)
    return app