from flask import render_template, flash, redirect, url_for

from app.firestore_service import get_todos, put_todo, delete_todo
from app.forms import TodoForm

from flask_login import login_required, current_user


from . import tasks


# Private Area Example
@tasks.route('/list', methods=['GET', 'POST'])
@login_required
def list():
  user_id = current_user.id

  task_form = TodoForm()

  if task_form.validate_on_submit():
    put_todo(user_id, task_form.description.data)
    flash('New Task created!', 'success')
    return redirect(url_for('tasks.list'))

  context = {
    'todos': get_todos(user_id),
    'task_form': task_form
  }
  return render_template('tasks.html', **context)


@tasks.route('/delete/<string:todo_id>', methods=['GET'])
@login_required
def delete(todo_id):
  user_id = current_user.id
  delete_todo(user_id=user_id, todo_id=todo_id)

  flash('Task removed', 'success')

  return redirect(url_for('tasks.list'))
