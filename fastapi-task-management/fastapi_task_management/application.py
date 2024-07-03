from fastapi_task_management.config.database import get_db
from fastapi_task_management.domain.dto.dtos import TaskCreateDTO, TaskUpdateDTO
from fastapi_task_management.domain.model.models import Task
from fastapi_task_management.repository.task_repository import TaskRepository
from fastapi_task_management.service.task_service import TaskService

def main():
    with get_db() as session:
        task_repository = TaskRepository(session=session)
        task_service = TaskService(task_repository)

        # Create
        task_created = TaskCreateDTO(
            title = 'Completar aula 1',
            description = 'Completar as instruções da aula 1',
            status = 'Em Progresso'
        )

        task_to_create = task_service.create(task_created)

        task_id = task_to_create.id
        print(f'task created with id: {task_id}')

        # Read
        task_read = task_service.read(task_id=task_id)
        print(f'task read: {task_read}')

        # Update
        task_update_data = TaskUpdateDTO(
            title='Novo Título',
            description= 'Nova Descrição',
            status= 'Pendente'
            )
        task_updated = task_service.update(task_id=task_id, task_data=task_update_data)
        print(f'task updated with id: {task_updated}')

        # Delete
        task_deleted_id = task_repository.delete(task_id=task_id)
        print(f'task deleted with id: {task_deleted_id}')

if __name__ == '__main__':
    main()