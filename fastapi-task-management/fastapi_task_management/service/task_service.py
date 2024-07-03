from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from fastapi_task_management.domain.dto.dtos import TaskDTO, TaskCreateDTO, TaskUpdateDTO
from fastapi_task_management.domain.model.models import Task
from fastapi_task_management.repository.task_repository import TaskRepository

class TaskService:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create(self, task_data: TaskCreateDTO) -> TaskDTO:
        task = Task(**task_data.model_dump())
        try:
            created = self.task_repository.save(task)
            return TypeAdapter(TaskDTO).validate_python(created)
        except IntegrityError as e:
            print(f'Erro ao criar tarefa: {task_data.model_dump()}. Erro: {str(e)}')

    def _read(self, task_id: int) -> Task:
        task = self.task_repository.read(task_id)
        if task is None:
            raise Exception(f'Tarefa {task_id} não Encontrada')
        return task

    def read(self, task_id: int) -> Task:
        return TypeAdapter(TaskDTO).validate_python(self._read(task_id))
    
    def find_all(self) -> list[TaskDTO]:
        tasks = self.task_repository.find_all()
        return [TypeAdapter(TaskDTO).validate_python(task) for task in tasks]
    
    def update(self, task_id: int, task_data: TaskUpdateDTO):
        task = self._read(task_id)
        task_data = task_data.model_dump(exclude_unset=True)
        for key, value in task_data.items():
            setattr(task, key, value)
        task_updated = self.task_repository.save(task)
        return TypeAdapter(TaskDTO).validate_python(task_updated)
    
    def delete(self, task_id: int) -> int:
        task = self._read(task_id)
        self.task_repository.delete(task)
        return task_id