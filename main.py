import unittest
from flask import request, make_response, redirect, render_template, session, url_for,flash
from flask_login import login_required, current_user


from app import create_app
from app.forms import TodoForm
from app.firestore_service import get_users, get_todos, put_todo

app = create_app()

#todos = ['Estudiar pipenv', 'Practicar behave', 'Implementar excepciones']

@app.cli.command()
def test():
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(test)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route ('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    #response.set_cookie('user_ip', user_ip)
    session['user_ip'] = user_ip

    return response

@app.route ('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    #user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()

    context = {
        'user_ip': user_ip,
        'todos' : get_todos(user_id=username),
        'username' : username,
        'todo_form': todo_form
    }

    if todo_form.validate_on_submit():
        put_todo(username, todo_form.description.data)

        flash('La tarea creada con éxito!')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)