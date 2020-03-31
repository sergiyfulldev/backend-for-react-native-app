from flask import Blueprint, request, jsonify, abort, url_for, current_app
from flask_mail import Message
from itsdangerous import BadSignature

from mobile.extensions import bcrypt, db, mail
from mobile.models import User
from mobile.utils import decode_auth_token, encode_auth_token, generate_email_token, \
    decode_email_token

auth = Blueprint("auth", __name__)


@auth.route('/verify/<payload>', methods=['GET'])
def verify(payload):
    try:
        _payload = decode_email_token(payload)
    except BadSignature:
        return jsonify({
            'status': 'error',
            'message': 'Invalid payload'
        }), 400

    user = User.query.filter_by(email=_payload['uid']).first()

    if user is None:
        return jsonify({
            'status': 'error',
            'message': 'Invalid User Id',
            'payload': _payload
        })

    user.verified = True

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Email Verified'
    })


@auth.route('/check/<token>', methods=['GET'])
def authentication_check(token):
    if token is None:
        return jsonify({
            'status': 'error',
            'message': "No token provided"
        }), 400

    token = decode_auth_token(token)

    if token is False:
        return jsonify({
            'status': "error",
            'message': 'Invalid / Expired Token'
        })

    return jsonify({
        'status': 'success',
        'message': "Token is valid"
    })


@auth.route('/register/', methods=['POST'])
def register():
    rjson = request.get_json()

    if rjson is None:
        return jsonify({
            'status': 'error',
            'message': 'No data provided in request'
        }), 400

    email = rjson.get('email')
    password = rjson.get('password')
    name = rjson.get('name')

    user = User.query.filter_by(email=email).first()

    if user is not None:
        return jsonify({
            'status': 'error',
            'message': 'This email has already been registered'
        }), 400

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=encrypted_password, name=name)

    # todo add skills as part of the registration process.

    db.session.add(user)
    db.session.commit()

    email_token = generate_email_token(email)

    message = Message(subject="Verify your Email", recipients=[user.email],
                      body="{0}".format(url_for(".verify", payload=email_token, _external=True)))
    mail.send(message)

    _payload = {
        'status': 'success',
        'message': 'Registration complete',
        'token': encode_auth_token(user.id).decode(),
    }

    if current_app.config['TESTING'] == True:
        _payload['email_token'] = email_token.decode()

    return jsonify(_payload)


@auth.route('/login/', methods=['POST'])
def authenticate():
    rjson = request.get_json()

    if rjson is None:
        return jsonify({
            'status': "error",
            "message": "No data was present in the request"
        }), 400

    email = rjson.get('email').lstrip().rstrip()
    password = rjson.get('password')

    if email is None or password is None:
        return jsonify({
            'status': 'error',
            'message': "Invalid login credentials"
        })

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({
            'status': 'error',
            'message': "Invalid login credentials",
        })

    user_password = user.password
    user_password = str(user_password)

    try:
        if not bcrypt.check_password_hash(user_password, password):
            return jsonify({
                'status': 'error',
                'message': 'Invalid login credentials'
            })
    except Exception as ex:
        return jsonify({
            'status': 'error',
            'message': "Invalid login credentials (Error Processing)",
            'user_password_type': str(type(user.password)),
            'json_password_type': str(type(password))
        })

    return jsonify({
        'status': 'success',
        'message': 'Login Successful',
        'token': encode_auth_token(user.id).decode("utf-8")
    })
