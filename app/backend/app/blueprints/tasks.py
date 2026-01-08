from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db.models import Task, Project, Status, Priority
from datetime import datetime
from app.db.extensions import db


## CONSTANTS

## HELPER FUNCTIONS
def project_exist(project_id:int,user_id:int) -> bool:
    projects = (Project
                    .query
                    .filter_by(
                        user_id=user_id
                    ).all())
     
    project_exist = False
        
    for project in projects:
        if project_id == project.__json__()['id']:
            project_exist = True
    return project_exist

## MAIN 

tasks_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/project"
)

@tasks_bp.get("/<int:project_id>/task")
@jwt_required()
def get_all_tasks(project_id):
    try:
        user_id =  get_jwt_identity()
            
        if not project_exist(project_id=project_id,user_id=user_id):
            return {
                "message":"There is no project with this id"
            },404
                
        
        tasks = Task.query.filter_by(
            project_id=project_id
        ).all()
        
        if tasks == []:
            return {
                "message":"No task in this project",
                "id":project_id
            },404
        
        res_tasks = [task.__json__() for task in tasks ]
        print(res_tasks)
        
        return{
            "tasks":res_tasks
        },200
    except Exception as e:
        return {
            "message":f"{e}"
        } ,400
        
    
@tasks_bp.post("/<int:project_id>/task")
@jwt_required()
def add_new_tasks(project_id):
    try :
        user_id = get_jwt_identity()
        data = request.json
        
        
        if not project_exist(project_id=project_id,user_id=user_id):
                return {
                    "message":"There is no project with this id"
                },404
                
                
        name = data["name"]
        desc = data["desc"]
        
        # Setting Status value  
        
        match data["status"]:
            case "to-do" :
                status = Status.TO_DO
            case "in-progress":
                status = Status.IN_PROGRESS
            case "done" :
                status = Status.DONE
            case _ :
                return {
                    "message":"Please provide a valid Status from ['to-do','in-progress','done']"
                },409
                
        # Setting Priority value 
            
        match data["priority"]:
            case "low" :
                priority  = Priority.LOW
            case "medium":
                priority = Priority.MEDIUM
            case "high" :
                priority = Priority.HIGH
            case _ :
                return {
                    "message":"Please provide a valid Priority from ['low','medium','high']"
                },409
        
        due_date = data["due_date"]
        
        
        ## Check if task with same name exist in the project 
        
        task_exist = (True if (Task
                    .query
                    .filter_by(
                        name = name,
                        project_id = project_id
                    ).first()) else False )
        
        print(task_exist)
        
        if task_exist :
            return {
                "message":"a task with same nane exists in this project."
            } , 409
            
            
        new_task = Task()
        new_task.name = name
        new_task.description = desc
        new_task.status = status
        new_task.priority = priority
        new_task.due_date = datetime.strptime(due_date,"%d-%m-%Y").date()
        new_task.project_id = project_id
        
        db.session.add(new_task)
        db.session.commit()
        
        return {
            "message":"New Task created successfully"
        },201
        
    except Exception as e :
        return {
            "error":str(e)
        },400
    
   
   #TODO : Make a put to update the task
@tasks_bp.put("/<int:project_id>/task/<int:task_id>")
@jwt_required()
def update_task(project_id,task_id):
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if not project_exist(project_id=project_id,user_id=user_id):
            return {
                "message":"There is no project with this id"
            },404
            
        task = (Task
                    .query
                    .filter_by(
                        id=task_id,
                        project_id=project_id
                    ).first())
        
        if not task:
            return {
                "message":"There is no task with this id in this project"
            },404
            
        name = data["name"]
        desc = data["desc"]
        
        # Setting Status value  
        
        match data["status"]:
            case "to-do" :
                status = Status.TO_DO
            case "in-progress":
                status = Status.IN_PROGRESS
            case "done" :
                status = Status.DONE
            case _ :
                return {
                    "message":"Please provide a valid Status from ['to-do','in-progress','done']"
                },409
                
        # Setting Priority value 
            
        match data["priority"]:
            case "low" :
                priority  = Priority.LOW
            case "medium":
                priority = Priority.MEDIUM
            case "high" :
                priority = Priority.HIGH
            case _ :
                return {
                    "message":"Please provide a valid Priority from ['low','medium','high']"
                },409
        
        due_date = data["due_date"]
        
        task.name = name
        task.description = desc
        task.status = status
        task.priority = priority
        task.due_date = datetime.strptime(due_date,"%d-%m-%Y").date()
        
        db.session.commit()
        
        return {
            "message":"Task updated successfully"
        },200
        
    except Exception as e :
        return {
            "error":str(e)
        },400

   
   
   #TODO : Make a delete to delete the task      
@tasks_bp.delete("/<int:project_id>/task/<int:task_id>")
@jwt_required()
def delete_task(project_id,task_id):
    try:
        user_id = get_jwt_identity()
        
        if not project_exist(project_id=project_id,user_id=user_id):
            return {
                "message":"There is no project with this id"
            },404
            
        task = (Task
                    .query
                    .filter_by(
                        id=task_id,
                        project_id=project_id
                    ).first())
        
        if not task:
            return {
                "message":"There is no task with this id in this project"
            },404
            
        db.session.delete(task)
        db.session.commit()
        
        return {
            "message":"Task deleted successfully"
        },200
        
    except Exception as e :
        return {
            "error":str(e)
        },400