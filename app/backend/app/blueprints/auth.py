from flask import Blueprint, request, jsonify
from app.schema.auth_schema import RegisterSchema, LoginSchema
from app.db.models import User
from app.db.extensions import db

from flask_jwt_extended import create_access_token

from marshmallow.exceptions import ValidationError

auth_bp = Blueprint(name = "auth",import_name=__name__,url_prefix="/auth")


## CONSTANTS

## HELPER FUNCTIONS

## MAIN ROUTES 

@auth_bp.post('/register')
def register():
        try :
                print(request.json)
                data = RegisterSchema().load(request.get_json())
                
               
        except ValidationError as err:
               return {
            "error": "Validation failed",
            "messages": err.messages
        }, 400
               
        if User.query.filter_by(username=data["username"]).first():
                        return {"error": "User already exists"}, 409

        user = User(username=data["username"])
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201


@auth_bp.post('/login')
def login():
        data = LoginSchema().load(request.json)

        user : User = User.query.filter_by(username=data["username"]).first()
        if not user or not user.check_password(data["password"]):
                return {"error": "Invalid credentials"}, 401

        token = create_access_token(
                identity=str(user.id),
                additional_claims={
                        "username": user.username
                        })

        return {
                "username":user.username,
                "access_token": f"Bearer {token}"
        }, 200

@auth_bp.route('/logout',methods=['GET'])
def logout():
        
        return jsonify({
                "message":"Logout OK"
        }) , 200