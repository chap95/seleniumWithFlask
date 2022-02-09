export FLASK_APP=flaskr
export FLASK_ENV=development
flask db init
flask db migrate -m "Initial migration."
flask db upgrade