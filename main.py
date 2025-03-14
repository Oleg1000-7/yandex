from data import db_session
from data.users import User

db_session.global_init("db/database.db")

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
