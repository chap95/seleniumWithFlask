from flask import Blueprint


bp = Blueprint('main', __name__, url_prefix='/api')


@bp.route('/test')
def test():
    return 'teset'
