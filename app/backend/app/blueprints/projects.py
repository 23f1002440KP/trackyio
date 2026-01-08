from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt

from app.db.extensions import db
from app.db.models import Project

from marshmallow.exceptions import ValidationError
from app.schema.project_schema import ProjectSchema

from datetime import datetime

projects_bp = Blueprint(
    name = "project",
    import_name=__name__,
    url_prefix="/project"
)

## CONSTANTS

## HELPER FUNCTIONS

## MAIN ROUTES 
@projects_bp.get("/")
@jwt_required()
def all_projects():
    try:
        user = get_jwt_identity()
        username = get_jwt()['username']
        
        
        projects = Project.query.filter_by(user_id=user).all()
        
       
        
        res_projeects = [project.__json__() for project in projects]
        
            
        
        return jsonify({
            "user": user,
            "username":username,
            "projects":res_projeects
        }),200
        
        
    except Exception as e :
        return {
            "message":str(e)
        },400
        
        
@projects_bp.get("/<int:project_id>")
@jwt_required()
def project_by(project_id):
    try:
        user = get_jwt_identity()
        username = get_jwt()['username']
        
        
        
        
        project = (Project
                   .query
                   .filter_by(
                       user_id=user,
                       id=int(project_id)
                       )
                   .first())
        
        if project is None :
            return {
                "message":"project with this id is not available"
            },404
            
            
        return jsonify({
            "user": user,
            "username":username,
            "project":project.__json__()
        }),200
        
        
    except Exception as e :
        return {
            "message":str(e)
        },400
        
        
        
@projects_bp.post("/")
@jwt_required()
def add_new_project():
    try:  
        project_data = ProjectSchema().load(request.json)
        id = get_jwt_identity()
        
                        
        p_name = project_data['name']
        desc = project_data['desc']
        github_link = project_data['github_link']
        due_date = project_data['due_date']
        
        p_user_id = int(id) 
        # pass
        project_exists = True if len(Project
                                     .query
                                     .filter_by(
                                         name=p_name,
                                         user_id=p_user_id
                                         )
                                     .all()) > 0 else False
        
        if project_exists :
            return {
                "message":"a project under this name already exist!"
            },409
            
       
        new_project = Project()
        new_project.name = p_name
        
        new_project.description = desc
        
        new_project.github_link = github_link
        
        new_project.due_date = datetime.strptime(due_date, "%d-%m-%Y").date()
       
        new_project.user_id = p_user_id
        
        
        db.session.add(new_project)
        db.session.commit() 
              
        return {
            "message":"New project created sucessfully "
        },201
    except Exception as ee :
        return {
            "message":str(ee)
        },400
    
   
   
   #TODO : Make a put to update the projects
@projects_bp.put("/<int:project_id>")
@jwt_required()
def update_project(project_id):
    try:
        project_data = ProjectSchema().load(request.json)
        user_id = get_jwt_identity()
        
        project = (Project
                   .query
                   .filter_by(
                       id=project_id,
                       user_id=user_id
                       )
                   .first())
        
        if project is None :
            return {
                "message":"project with this id is not available"
            },404
            
        project.name = project_data['name']
        project.description = project_data['desc']
        project.github_link = project_data['github_link']
        project.due_date = datetime.strptime(project_data['due_date'], "%d-%m-%Y").date()
        
        db.session.commit()
        
        return {
            "message":"Project updated successfully"
        },200
        
    except ValidationError as err:
               return {
            "error": "Validation failed",
            "messages": err.messages
        }, 400
    except Exception as e :
        return {
            "message":str(e)
        },400
   
   
   #TODO : Make a delete to delete the projects   
@projects_bp.delete("/<int:project_id>")
@jwt_required()
def delete_project(project_id):
    try:
        user_id = get_jwt_identity()
        
        project = (Project
                   .query
                   .filter_by(
                       id=project_id,
                       user_id=user_id
                       )
                   .first())
        
        if project is None :
            return {
                "message":"project with this id is not available"
            },404
            
        db.session.delete(project)
        db.session.commit()
        
        return {
            "message":"Project deleted successfully"
        },200
        
    except Exception as e :
        return {
            "message":str(e)
        },400