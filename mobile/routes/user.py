from flask import Blueprint, request, jsonify

from mobile.utils import validate_auth_token, get_user

from mobile.models import User, UserJobExperience, JobCategory, UserSkills

from mobile.extensions import db

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/info/',methods=['GET'])
@validate_auth_token
def index():
    user = get_user(request)

    return jsonify({
        'status': 'success',
        'message': '',
        'user': user.to_dict()
    })

@user_blueprint.route('/skills/',methods=['POST','DELETE'])
@validate_auth_token
def user_skills_endpoint():
    user = get_user(request)

    rjson = request.get_json()

    if rjson is None:
        return jsonify({
            'status': 'error',
            'message': 'No payload provided'
        })

    if request.method == "DELETE":
        skill = rjson.get('skill')

        user_skill = UserSkills.query.filter_by(user_id=user.id,name=skill).first()

        if user_skill is None:
            return jsonify({
                'status': 'error',
                'message': 'Invalid skill'
            })

        db.session.delete(user_skill)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Skill deleted'
        })

    if request.method == "POST":
        skill = rjson.get('skill')

        user_skill = UserSkills.query.filter_by(user_id=user.id,name=skill).first()

        if user_skill is not None:
            return jsonify({
                'status': 'error',
                'message': 'User skill already exists'
            })


        user_skill = UserSkills(user_id=user.id,name=skill)

        user.skills.append(user_skill)

        db.session.add(user_skill)
        db.session.add(user)

        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Skill Added'
        })

@user_blueprint.route('/about/',methods=['POST'])
@validate_auth_token
def update_user_about():
    user = get_user(request)

    rjson = request.get_json()

    if rjson is None:
        return jsonify({
            'status': 'error',
            'message': 'No payload present'
        })

    about = rjson.get('about')

    if about is None or len(about) == 0:
        return jsonify({
            'status': 'error',
            'message': 'Please include "about" field.'
        })

    user.about = about
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'About updated'
    })

@user_blueprint.route('/experience/',methods=['POST'])
@validate_auth_token
def add_user_skills_experience():
    user = get_user(request)
    rjson = request.get_json()

    if rjson is None:
        return jsonify({
            'status': 'error',
            'message': 'No data present in the request'
        })

    skills = rjson.get('skills')

    if skills is None or len(skills) == 0:
        return jsonify({
            'status': 'error',
            'message': "Invalid Payload"
        })

    for _skill in skills:
        job_cat_id = _skill['id']
        years_experience = _skill['years_experience']

        job_cat = JobCategory.query.filter_by(id=job_cat_id).first()

        if job_cat is None:
            return jsonify({
                'status': 'error',
                'message': 'Invalid job category id'
            })

        user_experience = UserJobExperience.query.filter_by(user_id=user.id,job_category=job_cat).first()

        if user_experience is None:
            user.job_experience.append(UserJobExperience(job_category=job_cat,years_experience=years_experience))
        else:
            user_experience.years_experience = years_experience
            db.session.add(user_experience)
        db.session.add(user)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Experience updated'
    })
