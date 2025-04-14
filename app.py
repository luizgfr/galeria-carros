from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
from config import *

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM imagens")
    imagens = cur.fetchall()
    return render_template('index.html', imagens=imagens)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['imagem']
        nome = request.form['nome']
        if file and allowed_file(file.filename):
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(caminho)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO imagens (nome, caminho) VALUES (%s, %s)", (nome, file.filename))
            mysql.connection.commit()
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT caminho FROM imagens WHERE id = %s", (id,))
    imagem = cur.fetchone()

    if imagem:
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], imagem[0])
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

        cur.execute("DELETE FROM imagens WHERE id = %s", (id,))
        mysql.connection.commit()
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        novo_nome = request.form['nome']
        cur.execute("UPDATE imagens SET nome = %s WHERE id = %s", (novo_nome, id))
        mysql.connection.commit()
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM imagens WHERE id = %s", (id,))
    imagem = cur.fetchone()
    return render_template('edit.html', imagem=imagem)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
