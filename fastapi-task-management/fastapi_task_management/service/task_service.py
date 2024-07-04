import logging
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from fastapi_task_management.domain.dto.dtos import TaskDTO, TaskCreateDTO, TaskUpdateDTO
from fastapi_task_management.domain.model.models import Task
from fastapi_task_management.repository.task_repository import TaskRepository

logger = logging.getLogger("fastapi")

class TaskService:

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create(self, task_data: TaskCreateDTO) -> TaskDTO:
        logger.info("Criando nova Tarefa")
        task = Task(**task_data.model_dump())
        try:
            created = self.task_repository.save(task)
            return TypeAdapter(TaskDTO).validate_python(created)
        except IntegrityError as e:
            logger.error(f'Erro ao criar tarefa: {task_data.model_dump()}')
            raise HTTPException(status_code=409, detail=f'Erro ao criar tarefa: {e.args[0]}')

    def _read(self, task_id: int) -> Task:
        task = self.task_repository.read(task_id)
        if task is None:
            logger.error(f'Tarefa {task_id} não encontrada')
            raise HTTPException(status_code=404,
                                detail=f'Tarefa {task_id} não Encontrada')
        return task

    def read(self, task_id: int) -> Task:
        logger.info(f'Buscando Tarefa de id:{task_id}')
        return TypeAdapter(TaskDTO).validate_python(self._read(task_id))
    
    def find_all(self) -> list[TaskDTO]:
        logger.info('Buscando todas as Tarefas')
        tasks = self.task_repository.find_all()
        return [TypeAdapter(TaskDTO).validate_python(task) for task in tasks]
    
    def update(self, task_id: int, task_data: TaskUpdateDTO):
        task = self._read(task_id)
        task_data = task_data.model_dump(exclude_unset=True)
        try:
            for key, value in task_data.items():
                setattr(task, key, value)
            task_updated = self.task_repository.save(task)
            return TypeAdapter(TaskDTO).validate_python(task_updated)
        except IntegrityError as e:
            logger.error(f'Erro ao atualizar tarefa: {task_data}')
            raise HTTPException(status_code=409, detail=f'Erro ao atualizar tarefa: {e.args[0]}')

    def delete(self, task_id: int) -> int:
        logger.info(f'Deletando tarefa {task_id}')
        task = self._read(task_id)
        self.task_repository.delete(task)
        return task_id