import flask
from . import db_session, correct_image
from .users import User

token = correct_image.an_interesting_variable

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route(f'/api/{token}/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users_list = db_sess.query(User).all()
    return flask.jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'login', 'email', 'created_date', 'is_premium'))
                 for item in users_list]
        }
    )


@blueprint.route(f'/api/{token}/users/<int:user_id_get>', methods=['GET'])
def get_one_user(user_id_get):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(user_id_get))
    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify(
        {
            f'user:{user_id_get}': [item.to_dict(only=('id', 'login', 'email', 'created_date', 'is_premium')) for
                                    item in
                                    user]
        }
    )


@blueprint.route(f'/api/{token}/users', methods=['POST'])
def create_user():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['login', 'email', 'created_date', 'is_premium']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    user = User(
        login=flask.request.json['login'],
        email=flask.request.json['email'],
        created_date=flask.request.json['created_date'],
        is_premium=flask.request.json['is_premium']
    )
    db_sess.add(user)
    db_sess.commit()
    return flask.jsonify({'id': user.id})


@blueprint.route(f'/api/{token}/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


