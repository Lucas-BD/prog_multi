from fastapi_task_management.config.database import get_db
from fastapi_task_management.model.models import Task

def main():
    title = 'Completar aula 1'
    description = 'Completar as instruções da aula 1'
    status = 'Em Progresso'

    with get_db() as session:
        task_data = {
            'title':title,
            'description':description,
            'status':status
        }

        # Create
        task = Task.create(session=session, **task_data)

        task_id = task.id
        print(f'task created with id: {task_id}')

        # Read
        task_read = Task.read(session=session, task_id=task_id)
        print(f'task read: {task_read}')

        # Update
        task_update_data = {'title':'Novo Titulo'}
        task_updated = Task.update(session=session, task_id=task_id, **task_update_data)
        print(f'task updated with id: {task_updated}')

        # Delete
        task_deleted_id = Task.delete(session=session, task_id=task_id)
        print(f'task deleted with id: {task_deleted_id}')

if __name__ == '__main__':
    main()