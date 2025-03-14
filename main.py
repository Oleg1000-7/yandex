import datetime

from data import db_session
from data.jobs import Jobs

db_session.global_init("db/database.db")

db_sess = db_session.create_session()

job = Jobs(
    team_leader=1,
    job="deployment of residential modules 1 and 2",
    work_size=15,
    collaborators="2, 3",
    start_date=datetime.datetime.now(),
    is_finished=False
)
db_sess.add(job)
db_sess.commit()