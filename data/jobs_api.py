from flask import jsonify, make_response, request, Blueprint

from data import db_session
from data.jobs import Jobs
from datetime import datetime

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=["GET", "POST"])
def jobs_f():
    db_sess = db_session.create_session()
    if request.method == "GET":
        jobs = db_sess.query(Jobs).all()
        return jsonify(
            {
                'jobs':
                    [item.to_dict(only=(
                        "id", "team_leader_id", "job", "work_size", "collaborators", "start_date", "end_date",
                        "is_finished"))
                        for item in jobs]
            }
        )

    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['team_leader_id', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
            return make_response(jsonify({'error': 'Bad request'}), 400)
        #if all([isinstance(i, j) for i, j in zip(request.json.values(), [int, str, int, str, ])])

        db_sess = db_session.create_session()
        job = Jobs(
            team_leader_id=request.json['team_leader_id'],
            job=request.json['job'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            start_date=datetime.fromisoformat(request.json['start_date']),
            end_date=datetime.fromisoformat(request.json['end_date']),
            is_finished=request.json['is_finished']
        )
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    if not isinstance(job_id, int):
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'job': job.to_dict(only=(
                "id", "team_leader_id", "job", "work_size", "collaborators", "start_date", "end_date", "is_finished"))
        }
    )
