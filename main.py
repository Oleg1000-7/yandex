from os.path import exists
from datetime import datetime

from data import db_session
from data.jobs import Jobs
from data.users import User
from flask import Flask, render_template


def create_db(db_sess):
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
        db_sess.commit()

    jobs_list = [Jobs(
        team_leader=1,
        job="deployment of residential modules 1 and 2",
        work_size=15,
        collaborators="2, 3",
        start_date=datetime.now(),
        is_finished=False
        ),
        Jobs(
            team_leader=1,
            job="deployment of residential modules 1 and 2",
            work_size=15,
            collaborators="2, 3",
            start_date=datetime.now(),
            is_finished=False
        ),
        Jobs(
            team_leader=1,
            job="deployment of residential modules 1 and 2",
            work_size=15,
            collaborators="2, 3",
            start_date=datetime.now(),
            is_finished=False
        )
    ]
    for job in jobs_list:
        db_sess.add(job)
        db_sess.commit()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

if not exists("db/database.db"):
    db_session.global_init("db/database.db")
    create_db(db_sess := db_session.create_session())
else:
    db_session.global_init("db/database.db")
    db_sess = db_session.create_session()

@app.route("/")
def index():
    jobs = db_sess.query(Jobs).all()
    return render_template("works_log.html", jobs_list=enumerate(jobs))

if __name__ == '__main__':
    app.run()
