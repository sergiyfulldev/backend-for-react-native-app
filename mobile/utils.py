import datetime
from functools import wraps

import jwt

from flask import abort, request, current_app, jsonify, make_response
from itsdangerous import URLSafeSerializer

from mobile.config import BaseConfig
from mobile.models import User, Permission

from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def isBlank(myString):
    """
    Check whether or not a string is blank
    :param myString: string to check
    :return: true if the string was blank, none, or all whitespace. False if there's content.
    """
    return not (myString and myString.strip())


def isNotBlank(myString):
    """
    Check whether or not a string is not blank.
    :param myString: string to check
    :return: true if the string has content other than whitespace
    """
    return bool(myString and myString.strip())


def get_user(request):
    """
    Helper method to retrieve a user based on the auth token passed via request headers
    :param request: request to retrieve the user object for
    :return: User or None
    """

    uid = get_user_id(request)

    if uid is None:
        return None

    user = User.query.filter_by(id=get_user_id(request)).first()

    return user


def get_user_id(request):
    """
    Retrieve a user id from decoding the authorization header payload and retrieving it.
    :param request: flask request object
    :return: user id if present.
    """

    value = None

    try:
        value = decode_auth_token(get_auth_token(request))['sub']
    except: #todo logging
        pass

    return value


def get_auth_token(request):
    """
    Retrieve an authorization bearer token if present inside the request headers
    :param request: flask request object
    :return: jwt token (serialized) if available in request headers
    """

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return None

    token = auth_header.split(' ')[1]

    return token


def requires_permission(node): # function with arg
    """
    Decorator for routes to require a permission node for access.
    This assumes they are authenticated aswell.
    :param node:
    :return:
    """

    def decorator(fn): #decorator for fn
        @wraps(fn)
        @validate_auth_token
        def decorated(*args, **kwargs):

            user = get_user(request)

            perms = user.permissions

            if len(perms) > 0:
                for perm in perms:
                    if perm.name.lower() == node.lower():
                        return fn(*args, **kwargs)

            return jsonify({
                'status': 'error',
                'message': 'Insufficient permissions'
            }), 401

        return decorated

    return decorator

def is_validated_user_request(request):
    """
    Checks whether or not the request passed is a validated user request by comparing the Authorization Header.
    :param request: request to check
    :return:
    """

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return False

# Split after 'Bearer '
    token = auth_header.split(' ')[1]

    payload = decode_auth_token(token)

    if payload is False: # If we has no payload.
        return False

    return True

def validate_auth_token(api_method):
    """
    Decorator to validate authentication token
    :param api_method:
    :return:
    """

    @wraps(api_method)
    def decorated_method(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if auth_header is None:
            return jsonify({
                'status': 'error',
                'message': "Unable to locate authorization header"
            }), 401

        # Split after 'Bearer '
        token = auth_header.split(' ')[1]

        payload = decode_auth_token(token)

        if payload is False:
            return jsonify({
                'status': 'error',
                'message': 'Expired session'
            }), 401

        return api_method(*args, **kwargs)

    return decorated_method


def decode_auth_token(token):
    try:
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # todo handle expired signature
        pass
    except jwt.InvalidTokenError:
        # todo invalid token error
        pass

    return False


def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
        }
        token = jwt.encode(payload, BaseConfig.SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        print(e)
        return e


def generate_email_token(user_id):
    try:
        payload = {
            'uid': user_id
        }

        token = jwt.encode(payload, "3m411")
        return token
    except:
        return False


def decode_email_token(token):
    try:
        payload = jwt.decode(token, '3m411')
        return payload
    except jwt.ExpiredSignatureError:
        # todo handle expired signature
        pass
    except jwt.InvalidTokenError:
        # todo invalid token error
        pass

    return False
