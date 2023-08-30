from datetime import datetime
from ariadne import convert_kwargs_to_snake_case
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from api import db
from .models import Todo

@convert_kwargs_to_snake_case
def resolve_create_todo(obj, info, description, due_date):
    try:
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        todo = Todo(
            description=description, due_date=due_date
        )
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format yyyy-mm-dd"]
        }
    return payload

@convert_kwargs_to_snake_case
def resolve_mark_done(obj, info, todo_id):
    try:
        query = select(Todo).where(Todo.id == todo_id)
        todo = db.session.execute(query).one()
        todo.completed = True
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except NoResultFound:
        print("No Result Found")
        payload = {
            "success": False,
            "errors":  [f"Todo matching id {todo_id} was not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def resolve_delete_todo(obj, info, todo_id):
    try:
        query = select(Todo).where(Todo.id == todo_id)
        todo = db.session.execute(query).one()
        delete_stmt = delete(Todo).where(Todo.id == todo_id)
        db.session.execute(delete_stmt)
        db.session.commit()
        payload = {"success": True}
    except NoResultFound:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }
    return payload

@convert_kwargs_to_snake_case
def resolve_update_due_date(obj, info, todo_id, new_date):
    try:
        query = select(Todo).where(Todo.id == todo_id)
        todo = db.session.execute(query).one()
        todo.due_date = datetime.strptime(new_date, '%Y-%m-%d').date()
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. Date should be in "
                       "the format yyyy-mm-dd"]
        }
    except NoResultFound:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }
    return payload
