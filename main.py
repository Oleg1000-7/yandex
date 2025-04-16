from os.path import exists
from datetime import datetime
from sqlalchemy.orm import Session

from data import db_session
from data.jobs import Jobs
from data.users import User
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required

from forms.login_form import LoginForm
from forms.register_form import RegisterForm


def create_db(db_sess: Session):
    user_list = [
        User(
            surname="Scott",
            name="Ridley",
            age=21,
            position="captain",
            speciality="research engineer",
            address="module_1",
            email="scott_chief@mars.org"
        ),
        User(
            surname="Ivanov",
            name="Ivan",
            age=25,
            position="mate",
            speciality="mechanic",
            address="module_1",
            email="II_mate@mars.org"
        ),
        User(
            surname="Sergey",
            name="Sokolov",
            age=32,
            position="crew",
            speciality="engineer",
            address="module_2",
            email="SerSok@mars.org"
        ),
        User(
            surname="Nikita",
            name="Lvov",
            age=22,
            position="crew",
            speciality="medic",
            address="module_2",
            email="QWE@mars.org"
        )
    ]
    for user in user_list:
        db_sess.add(user)

    jobs_list = [Jobs(
        team_leader_id=1,
        job="deployment of residential modules 1 and 2",
        work_size=15,
        collaborators="2, 3",
        start_date=datetime.now(),
        is_finished=False
    ),
        Jobs(
            team_leader_id=1,
            job="deployment of residential modules 3 and 4",
            work_size=12,
            collaborators="4, 5",
            start_date=datetime.now(),
            is_finished=False
        )
    ]
    for job in jobs_list:
        db_sess.add(job)
    db_sess.commit()


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret_key'

if not exists("db/database.db"):
    db_session.global_init("db/database.db")
    create_db(db_sess := db_session.create_session())

else:
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    jobs = db_sess.query(Jobs).all()
    return render_template("works_log.html", jobs_list=enumerate(jobs, start=1))


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
                surname = form.surname.data,
                name = form.name.data,
                age = form.age.data,
                position = form.position.data,
                speciality = form.speciality.data,
                address = form.address.data,
                email = form.email.data,
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
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run()
