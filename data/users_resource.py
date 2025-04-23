from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.users import User


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    users = session.query(User).get(news_id)
    if not users:
        abort(404, message=f"News {news_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True, type=str)
parser.add_argument('speciality', required=True, type=str)
parser.add_argument('address', required=True, type=str)
parser.add_argument('email', required=True, type=str)
parser.add_argument('password', required=True, type=str)
parser.add_argument('modified_date', type=str)


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_news_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({'user': users.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'address', 'modified_date'))})

    def delete(self, users_id):
        abort_if_news_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'modified_date')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            modified_date=args['modified_date']
        )
        users.set_password(args["password"])
        session.add(users)
        session.commit()
        return jsonify({'id': users.id})
