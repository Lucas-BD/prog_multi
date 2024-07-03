from sqlalchemy.orm import Session

from fastapi_task_management.domain.model.models import Task

class TaskRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, task: Task):
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def read(self, task_id: int):
        return self.session.query(Task).filter(Task.id == task_id).first()
    
    def delete(self, task: Task):
        self.session.delete(task)
        self.session.commit()
    
    def find_all(self):
        return self.session.query(Task).all()