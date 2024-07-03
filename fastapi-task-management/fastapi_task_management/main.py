from fastapi_task_management.config.database import get_db
from fastapi_task_management.model.models import Task
from fastapi_task_management.repository.task_repository import TaskRepository

def main():
    with get_db() as session:
        task_repository = TaskRepository(session=session)

        task_data = {
            'title': 'Completar aula 1',
            'description': 'Completar as instruções da aula 1',
            'status': 'Em Progresso'
        }

        # Create
        task_to_create = Task(**task_data)
        task = task_repository.create(task_to_create)

        task_id = task.id
        print(f'task created with id: {task_id}')

        # Read
        task_read = task_repository.read(task_id=task_id)
        print(f'task read: {task_read}')

        # Update
        task_update_data = {'title':'Novo Titulo'}
        task_updated = task_repository.update(task_id=task_id, **task_update_data)
        print(f'task updated with id: {task_updated}')

        # Delete
        task_deleted_id = task_repository.delete(task_id=task_id)
        print(f'task deleted with id: {task_deleted_id}')

if __name__ == '__main__':
    main()