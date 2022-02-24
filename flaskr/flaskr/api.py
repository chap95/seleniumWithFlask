from flask import Blueprint
from flask import app

bp = Blueprint('main', __name__, url_prefix='/api')


@bp.test('/test')
def test():
    return 'teset'
