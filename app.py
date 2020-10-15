from flask import (Flask, render_template, request, url_for, redirect, flash)
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'vanov'
app.config['MYSQL_PASSWORD'] = 'Allheilvon11$'
app.config['MYSQL_DB'] = 'larapi'
app.secret_key = 'sahkdksbfksbkfbsk'
mysql = MySQL(app)


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT posts.id, users.name, posts.content FROM posts INNER JOIN users ON posts.user_id=users.id ORDER BY posts.id DESC")
    posts = cur.fetchall()
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts, users=users)


@app.route('/save', methods=["POST"])
def save():
    user_id = request.form['user']
    post = request.form['post']

    cur = mysql.connection.cursor()
    query  = "INSERT INTO posts (user_id, content) VALUES ('{}', '{}')".format(user_id, post)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash('sukses tambah', 'success')
    return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    query  = "DELETE FROM posts WHERE id = {}".format(id)
    cur.execute(query)
    mysql.connection.commit()
    cur.close()
    flash('sukses delete', 'delete')
    return redirect(url_for('home'))