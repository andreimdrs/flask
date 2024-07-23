from flask import Flask, render_template, make_response, url_for, request, session, redirect, jsonify
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = b'\xe7\xf7\x8c\xea\x0c\xd9\xeb\xbc\x90\xd3\xbd7Pf\x97\xe6\x0f@\x1d\x90\x12\xf5\xb7'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods= ['GET', 'POST'])
def forms():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        expiracao = datetime.utcnow() + timedelta(days=365 * 10)
        expiracao_format_cookie = expiracao.timestamp()
        response = make_response('cookie definido')
        response.set_cookie('username', nome, expires=expiracao_format_cookie)
        response.set_cookie('email', email, expires=expiracao_format_cookie)
        response.set_cookie('number', telefone, expires=expiracao_format_cookie)
        response.set_cookie('password', senha, expires=expiracao_format_cookie)
        return response 

@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:

        v = request.form['nome']
        v2 = request.form['email']
        v3 = request.form['telefone']
        v4 = request.form['senha']

        data = {
            'nome' : v,
            'email' : v2,
            'nmr' : v3,
            'senha' : v4
        }

        dados = {
            'nome': request.cookies.get('username'),
            'email': request.cookies.get('email'),
            'nmr': request.cookies.get('number'),
            'senha': request.cookies.get('senha'),
        }

        for chave in dados:
            if chave in data:
                if dados[chave] != data[chave]:
                    return "Não logado!"
                else:
                    session['user'] = dados['nome']
                    session['password'] = dados['senha']
                    return redirect (url_for('dashboard'))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/backup')
def backup():
    username = request.cookies.get('username')
    email = request.cookies.get('email')
    number = request.cookies.get('number')
    password = request.cookies.get('password')

    cookie_info = {
            'username': username,
            'email': email,
            'number': number,
            'password': password,
        }

    arquivo = 'cookie_info.json'

    with open(arquivo, 'a') as f:
        json.dump(cookie_info, f)

    response = make_response(f'Dados salvos em {arquivo}, retorne a dashboard!')
    return response

@app.route('/comments', methods=['POST'])
def comments():
    user = session['user']
    comentario = request.form['comment']

    envio = {
        'user': user,
        'comentario': comentario,
    }

    arquivo = 'cookie_info.json'

    with open(arquivo, 'a') as f:
        json.dump(envio, f)
    
    response = make_response('Seu comentário foi salvo! Retorne a dashboard.')
    return response