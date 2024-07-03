from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime
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