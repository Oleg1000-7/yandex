from data import db_session
from data.users import User

db_session.global_init(f"db/{input()}")

db_sess = db_session.create_session()

colonists = db_sess.query(User).filter(User.address == "module_1",
                                       User.speciality.notilike("%engineer%"), User.position.notilike("%engineer%"))

for colonist in colonists:
    print(colonist)
