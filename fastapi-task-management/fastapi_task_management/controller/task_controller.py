from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fastapi_task_management.config.database import get_db
from fastapi_task_management.domain.dto.dtos import TaskCreateDTO, TaskDTO, TaskUpdateDTO
from fastapi_task_management.repository.task_repository import TaskRepository
from fastapi_task_management.service.task_service import TaskService

task_router = APIRouter(prefix='/tasks', tags=['Tasks'])

def get_task_repository(session: Session = Depends(get_db)):
    return TaskRepository(session=session)

@task_router.post(path='/', 
                  status_code=201, 
                  description='Cria nova Tarefa',
                  response_model = TaskDTO)
async def create(
    request: TaskCreateDTO, 
    task_repo: TaskRepository = Depends(get_task_repository)
    ):
    task_service = TaskService(task_repo)
    return task_service.create(request)

@task_router.get('/{task_id}',
                 status_code=200,
                 description='Buscat Tarefa por id',
                 response_model=TaskDTO)
async def find_by_id(
    user_id: int, 
    task_repo: TaskRepository = Depends(get_task_repository)
    ):
    task_service = TaskService(task_repo)
    return task_service.read(user_id)

@task_router.get('/',
                 status_code=200,
                 description='Buscat todas as Tarefas',
                 response_model=list[TaskDTO])
async def find_all(
    task_repo: TaskRepository = Depends(get_task_repository)
    ):
    task_service = TaskService(task_repo)
    return task_service.find_all()

@task_router.put('/{task_id}',
                 status_code=200,
                 description='Atualizar Tarefa',
                 response_model=TaskDTO)
async def update_by_id(
    user_id: int, 
    task_data: TaskUpdateDTO,
    task_repo: TaskRepository = Depends(get_task_repository)
    ):
    task_service = TaskService(task_repo)
    return task_service.update(user_id, task_data)

@task_router.delete('/{task_id}',
                 status_code=204,
                 description='Deletar Tarefa por ID')
async def delete_by_id(
    user_id: int, 
    task_repo: TaskRepository = Depends(get_task_repository)
    ):
    task_service = TaskService(task_repo)
    task_service.delete(user_id)