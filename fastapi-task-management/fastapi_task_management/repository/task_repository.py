from sqlalchemy.orm import Session

from fastapi_task_management.model.models import Task

class TaskRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, task: Task):
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def read(self, task_id: int):
        return self.session.query(Task).filter(Task.id == task_id).first()
    
    def update(self, task_id: int, **kwargs):
        task = self.read(task_id=task_id)
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            self.session.commit()
            self.session.refresh(task)
        return task_id
    
    def delete(self, task_id: int):
        task = task = self.read(task_id=task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
        return task_id