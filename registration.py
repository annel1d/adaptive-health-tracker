import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

DB_PATH = 'users-database.db'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные формы
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Проверяем соответствие паролей
        if password != confirm_password:
            return render_template('register.html', error='Пароли не совпадают')

        # Регистрируем пользователя в базе данных
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query = "INSERT INTO User (name, email, password) VALUES (?, ?, ?)"
        cursor.execute(query, (name, email, password))
        conn.commit()
        conn.close()

        return render_template('success.html', name=name)

    return render_template('register.html')
