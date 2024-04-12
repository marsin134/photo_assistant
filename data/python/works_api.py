import flask
from . import db_session
from .works import Works

blueprint = flask.Blueprint(
    'works_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/works')
def get_works():
    db_sess = db_session.create_session()
    works_list = db_sess.query(Works).all()
    print(works_list)
    return flask.jsonify(
        {
            'works':
                [item.to_dict(only=('id', 'user_id', 'type_works', 'name_file'))
                 for item in works_list]
        }
    )


@blueprint.route('/api/works/<int:user_id_get>', methods=['GET'])
def get_one_works(user_id_get):
    db_sess = db_session.create_session()
    works_list = db_sess.query(Works).filter(Works.user_id == int(user_id_get))
    if not works_list:
        return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)
    return flask.jsonify(
        {
            f'works_user_{user_id_get}': [item.to_dict(only=('id', 'user_id', 'type_works', 'name_file')) for item in
                                          works_list]
        }
    )
