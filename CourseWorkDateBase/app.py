from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# DB setup
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts ORDER BY id DESC')
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>')
def delete(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:post_id>', methods=['POST'])
def edit(post_id):
    title = request.form['title']
    content = request.form['content']
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)