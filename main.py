import unittest
from flask import request, make_response, redirect, render_template, session, url_for,flash
from flask_login import login_required


from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users, get_todos

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

@app.route ('/hello', methods=['GET'])
@login_required
def hello():
    #user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos' : get_todos(user_id=username),
        'username' : username,
    }

    return render_template('hello.html', **context)