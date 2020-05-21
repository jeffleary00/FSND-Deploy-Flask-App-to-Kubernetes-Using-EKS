"""
A simple app to create a JWT token.
"""

import os
import logging
import datetime
import functools
import jwt

# pylint: disable=import-error
from flask import Flask, jsonify, request, abort


JWT_SECRET = os.environ.get('JWT_SECRET', 'myjwtsecret')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


def _logger():
    """
    Setup logger format, level, and handler.

    RETURNS: log object
    """

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log.addHandler(stream_handler)
    return log


LOG = _logger()
LOG.debug("Starting with log level: %s" % LOG_LEVEL )
APP = Flask(__name__)

def require_jwt(function):
    """
    Decorator to check valid jwt is present.
    """

    @functools.wraps(function)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except: # pylint: disable=bare-except
            abort(401)

        return function(*args, **kws)
    return decorated_function


@APP.route('/', methods=['POST', 'GET'])
def health():
    return jsonify("Healthy")


@APP.route('/auth', methods=['POST'])
def auth():
    """
    Create JWT token based on email.
    """

    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')
    if not email:
        LOG.error("No email provided")
        return jsonify({"message": "Missing parameter: email"}, 400)
    if not password:
        LOG.error("No password provided")
        return jsonify({"message": "Missing parameter: password"}, 400)
    body = {'email': email, 'password': password}

    user_data = body

    return jsonify(token=_get_jwt(user_data).decode('utf-8'))


@APP.route('/contents', methods=['GET'])
def decode_jwt():
    """
    Check user token and return non-secret data
    """

    if not 'Authorization' in request.headers:
        abort(401)
    data = request.headers['Authorization']
    token = str.replace(str(data), 'Bearer ', '')
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except: # pylint: disable=bare-except
        abort(401)


    response = {'email': data['email'],
                'exp': data['exp'],
                'nbf': data['nbf'] }
    return jsonify(**response)


def _get_jwt(user_data):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    payload = {'exp': exp_time,
               'nbf': datetime.datetime.utcnow(),
               'email': user_data['email']}
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

if __name__ == '__main__':
    """
    TODO:
    For some reason, launching the development web server with IP address
    of 127.0.0.1 was causing this app to be unreachable when running in a
    docker container. It worked fine running standalone on client machine,
    but docker would not respond to requests, even with proper port mapping.

    Finally, realized that the example projects used 0.0.0.0 on all their
    development servers. So, I changed to that and now it is ok.

    We will see if it continues to work after enabling the gunicorn server.(?)
    """
    
    # APP.run(host='127.0.0.1', port=8080, debug=True)
    APP.run('0.0.0.0', port=8080, debug=True)
