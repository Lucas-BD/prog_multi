from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from fastapi_task_management.config.database import Base, engine

class Task(Base):
    __tablename__= "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(30))
    description = Column(String(100))
    status = Column(String(12))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (CheckConstraint(status.in_(['Pendente',
                                                  'Em Progresso',
                                                  'Concluída'])),)

    @staticmethod
    def create(session: Session, **kwargs):
        task = Task(**kwargs)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
    @staticmethod
    def read(session: Session, task_id: int):
        return session.query(Task).filter(Task.id == task_id).first()
    
    @staticmethod
    def update(session: Session, task_id: int, **kwargs):
        task = Task.read(session, task_id)
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
            session.commit()
            session.refresh(task)
        return task_id
    
    @staticmethod
    def delete(session: Session, task_id: int):
        task = Task.read(session, task_id)
        if task:
            session.delete(task)
            session.commit()
        return task_id
    
    def __repr__(self):
        return f'''
        <Task(
        id = {self.id},
        title = {self.title},
        description = {self.description},
        status = {self.status},
        created_at = {self.created_at}
        )>'''
    
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)