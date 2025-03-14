from datetime import datetime

from data import db_session
from data.jobs import Jobs
from data.users import User

db_session.global_init(f"db/{input()}")

db_sess = db_session.create_session()

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

job = Jobs(
    team_leader=1,
    job="deployment of residential modules 1 and 2",
    work_size=15,
    collaborators="2, 3",
    start_date=datetime.datetime.now(),
    is_finished=False
)
db_sess.add(job)

colonists = db_sess.query(User.id).filter(User.address == "module_1",
                                          User.speciality.notilike("%engineer%"),
                                          User.position.notilike("%engineer%")).all()

for colonist in colonists:
    print(colonist[0])
