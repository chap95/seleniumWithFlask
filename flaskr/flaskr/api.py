from flask import Blueprint, jsonify

bp = Blueprint('main', __name__, url_prefix='/api')


@bp.route('/test')
def test():
    return 'test'


@bp.route('/getResult')
def getResult():
    from flaskr import Result
    from flaskr import db
    data = []
    result = db.session.query(Result).all()
    print('### result db => ', result)
    print('### print => ', print)
    descriptionList = db.session.query(Result.description).all()
    print('description list => ', descriptionList)
    linkList = db.session.query(Result.link).all()
    print('### linkList =>', linkList)
    # for index in range(len(descriptionList)):
    #     print('### index -> ', descriptionList[index])
    #     description = descriptionList[index]
    #     print('type of description => ', type(description))
    #     if hasattr(description, 'replace'):
    #         description = description.replace('(', '')
    #         description = description.replace(')', '')
    #         description = description.replace('\'', '')
    #         description = description.replace(',', '')

    #     link = linkList[index]
    #     if(len(description) > 0):
    #         data.append({'description': description, 'link': link})

    # print('data -> ', jsonify(data))
    return jsonify(data)
