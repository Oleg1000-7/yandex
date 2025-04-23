from os.path import exists
from os import makedirs
from datetime import datetime

from flask_restful import Api
from sqlalchemy.orm import Session

from data import db_session, jobs_api, users_resource
from data.jobs import Jobs
from data.users import User
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required

from forms.job_create_form import JobCreateForm
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
api = Api(app)
app.register_blueprint(jobs_api.blueprint)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'secret_key'

if not exists("db/database.db"):
    makedirs("db")
    db_session.global_init("db/database.db")
    create_db(db_sess := db_session.create_session())

else:
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()

api.add_resource(users_resource.UsersListResource, '/api/v2/users')

api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')

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
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
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


@app.route("/addjob", methods=['GET', 'POST'])
def add_job():
    form = JobCreateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not db_sess.query(User).filter(User.id == form.team_leader_id.data).first():
            return render_template('add_job.html',
                                   message="Нет тимлида с введенным id",
                                   form=form)

        ids = set(map(int, form.collaborators.data.split(", ")))
        if len(db_sess.query(User).filter(User.id.in_(ids)).all()) == len(ids):
            job = Jobs(
                team_leader_id=form.team_leader_id.data,
                job=form.job.data,
                work_size=form.work_size.data,
                collaborators=form.collaborators.data,
                is_finished=form.is_finished.data
            )
            db_sess.add(job)
            db_sess.commit()

            return redirect("/")
        return render_template('add_job.html',
                               message="Нет пользователя с введенным id",
                               form=form)
    return render_template('add_job.html', title='Adding a job', form=form)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
