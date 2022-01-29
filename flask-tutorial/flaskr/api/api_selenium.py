import os
from flask import request, g
import uuid
from utils.utils import *


def get_selenium_result():
    if request.method == 'GET':

        data_cursor = g.db.execute("SELECT * ""FROM ResultTable")
        data = data_cursor.fetchall()
        result_data = [{
            'ID': row[0],
            'DESCRIPTION': row[1]
        }]

        return success_response(result_data)


def store_selenium_result(description: str):
    description_cursor = g.db.execute("SELECT * FROM "
                                      "ResultTable WHERE "
                                      "DESCRIPTION=?",
                                      description
                                      )

    if(description_cursor.fetchall() > 1):
        return success_message("해당 data 는 이미 존재")
    else:
        query = ('INSERT INTO ResultTable (ID, DESCRIPTION)'
                 'VALUSE (:ID, :DESCRIPTION);'
                 )

        param = {
            'ID': str(uuid.uuid4),
            'DESCRIPTION': description,
        }

        g.db.execute(query, param)
        g.db.commit()
        return success_response('', "These are the students "
                                "stored into records")
