import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.news import News
from data.users import User
from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def send_email(subject, message, from_email, to_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        if 'устал' in news.content.lower() or 'устал' in news.title.lower():
            send_email('Новая заметка добавлена',
                       'На сайте health-tracker была добавлена новая заметка. \n'
                       'Вы очень устали, Вам сегодня стоит лечь пораньше и не утруждать себя занятиями по дому. \n\n\n\nВаш HEALTH TRACKER',
                       'dima444obr@gmail.com',
                       current_user.email,
                       'rfncesluwulqsgnf')
        elif 'живот' in news.content.lower() or 'живот' in news.title.lower():
            send_email('Новая заметка добавлена',
                       'На сайте health-tracker была добавлена новая заметка. \n'
                       'Помогают снять боль в животе следующие медикаменты: \n'
                       'спазмолитики: Дротаверин, Но-шпа, Тримедат, Необутин \n'
                       'ферменты: Мезим форте, Креон, Фестал, Панкреатин, Эрмиталь. \n'
                       'антациды: Алмагель, Алмагель А, Гевискон, Ренни, Маалокс, Фосфалюгель \n'
                       'препараты висмута: Викаир, Викалин, Де-Нол \n'
                       'Возможно, Вы просто переели или отравилсь, Вам сегодня стоит лечь пораньше и не утруждать себя занятиями по дому. \n\n\n\nВаш HEALTH TRACKER',
                       'dima444obr@gmail.com',
                       current_user.email,
                       'rfncesluwulqsgnf')
        elif 'голов' in news.content.lower() or 'голов' in news.title.lower():
            send_email('Новая заметка добавлена',
                       'На сайте health-tracker была добавлена новая заметка. \n'
                       'При головных болях можно использовать разные препараты. \n'
                       'К ним относятся «Анальгин», «Парацетамол», «Панадол», «Баралгин», «Темпалгин», «Седальгин» и др. \n'
                       'С ярко выраженным эффектом. Это такие препараты, как «Аспирин», «Индометацин», «Диклофенак», «Ибупрофен», «Кетопрофен» и др. \n'
                       'Возможно, Вы просто очень устали, Вам сегодня стоит лечь пораньше и не утруждать себя занятиями по дому. \n\n\n\nВаш HEALTH TRACKER',
                       'dima444obr@gmail.com',
                       current_user.email,
                       'rfncesluwulqsgnf')
        elif 'хорош' in news.content.lower() or 'хорош' in news.title.lower() or 'замечательно' in news.content.lower() \
                or 'замечательно' in news.title.lower() or 'отлично' in news.content.lower() or 'отлично' in news.title.lower():
            send_email('Новая заметка добавлена',
                       'На сайте health-tracker была добавлена новая заметка. \n'
                       'Просто замечательно, когда чувствуешь себя хорошо, не так ли?. \n\n\n\nВаш HEALTH TRACKER',
                       'dima444obr@gmail.com',
                       current_user.email,
                       'rfncesluwulqsgnf')
        return redirect('/')
    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
