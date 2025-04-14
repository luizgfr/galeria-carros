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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
