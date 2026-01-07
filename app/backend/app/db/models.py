from .extensions import db
from .extensions import hash_password, verify_password, needs_rehash
from datetime import date
from enum import Enum


class Status(Enum):
    DONE = "done"
    IN_PROGRESS = "in-progress" 
    TO_DO = "to-do"
    
    def __str__(self):
        return self.value
    




class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    def __str__(self):
        return self.value
    
    

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    projects = db.relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password: str):
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)

    

class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    github_link = db.Column(db.String(120), nullable=True)
    created_on = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date, nullable=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )

    user = db.relationship("User", back_populates="projects")

    tasks = db.relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    
    def __json__(self):
        
        tasks = [task.__json__() for task in self.tasks]
        return {
            'description': self.description,
            'created_on': str(self.created_on),
             'name': self.name,
             'id': self.id,
             'github_link': self.github_link,
             'due_date': str(self.due_date),
             'tasks':tasks
             }

    
    
class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    status = db.Column(
        db.Enum(Status, name="status_enum"),
        nullable=False,
        default=Status.TO_DO
    )

    priority = db.Column(
        db.Enum(Priority, name="priority_enum"),
        nullable=False,
        default=Priority.LOW
    )

    created_on = db.Column(db.Date, default=date.today)
    due_date = db.Column(db.Date, nullable=True)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.id", ondelete="CASCADE"),
        nullable=False
    )

    project = db.relationship("Project", back_populates="tasks")
    
    
    def __json__(self):
        return {
            "name":self.name,
            "desc":self.description,
            "status":self.status.__str__(),
            "priority":self.priority.__str__(),
            "due_date":self.due_date,
            "created_on":self.created_on,
            "project_id":self.project_id
        }   
    
    
    
      
    
    
    