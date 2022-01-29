import os
from route_config import *

app.debug = True
host = os.environ.get('IP', '127.0.0.1')
port = int(os.environ.get('PORT', '5000'))
app.run(host=host, port=port)
