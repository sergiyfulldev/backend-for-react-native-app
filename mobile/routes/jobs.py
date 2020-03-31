from flask import Blueprint, jsonify, request, current_app

from mobile.extensions import db
from mobile.models import Job, JobApplication, User, JobCategory, JobType
from mobile.utils import validate_auth_token, decode_auth_token, get_auth_token, isBlank, get_user_id, get_user, \
    haversine, is_validated_user_request

jobs_blueprint = Blueprint('jobs', __name__)


# todo implement return variable if user has applied to job.

@jobs_blueprint.route('/categories', methods=['GET'])
def categories():
    categories = [category.to_dict() for category in JobCategory.query.all()]
    return jsonify({
        'status': 'success',
        'message': '',
        'categories': categories
    })

@jobs_blueprint.route('/search/', methods=['POST'])
@validate_auth_token
def search():
    # todo implement job title search.

    rjson = request.get_json()

    if rjson is None:
        return jsonify({
            'status': 'error',
            'message': 'No data provided'
        })

    user = get_user(request)

    search_options = rjson.get('search')

    # radius search variables
    radius_search = False
    radius_km = None
    user_long = None
    user_lat = None

    category = None
    job_type = None

    if 'radius' in search_options.keys():
        user_long = float(search_options['long'])
        user_lat = float(search_options['lat'])

        radius_km = search_options['radius']

        radius_search = True

    if 'category' in search_options.keys():
        category = search_options['category']

        category = JobCategory.query.filter_by(name=category).first()

        if category is None:
            return jsonify({
                'status': 'error',
                'message': 'Invalid category name provided',
                'payload': search_options
            }), 400

    if 'job_type' in search_options.keys():
        job_type = JobType.query.filter_by(name=search_options['job_type']).first()

        if job_type is None:
            return jsonify({
                'status': 'error',
                'message': 'Invalid job type provided',
                'payload': search_options
            }), 400

    if radius_search is False and (category is None or job_type is None):
        return jsonify({
            'status': 'error',
            'message': 'Please check your search settings and try again',
            'payload': search_options
        }), 400

    jobs = None
    # retrieve the jobs in this category

    if job_type is not None:
        jobs = job_type.jobs

    elif category is not None:
        jobs = category.jobs

    jobs = Job.query.all()

    jobs_found = []

    # todo look into reducing the list

    for job in jobs:

        # If doing a radius-based search, check the distance between the user and the jobs host location.
        if radius_search is True and haversine(float(job.longitude), float(job.latitude), user_long, user_lat) > int(
                radius_km):
            continue

        jobs_found.append(job.to_dict())

    return jsonify({
        'status': 'success',
        'message': '',
        'jobs': jobs_found,
        'search_settings': search_options
    })


@jobs_blueprint.route('/apply/', methods=['POST'])
@validate_auth_token
def apply():
    rjson = request.get_json()

    if rjson is None:
        return jsonify({
            'status': 'error',
            'message': "No data provided"
        }), 400

    job = Job.query.filter_by(id=rjson.get('id')).first()

    if job is None:
        return jsonify({
            'status': 'error',
            'message': 'Invalid Job ID'
        }), 400

    user = get_user(request)

    application = JobApplication.query.filter_by(user_id=user.id, job_id=job.id).first()

    if application is not None:
        return jsonify({
            'status': "error",
            'message': "An application has already been submitted for this job."
        }), 400

    user.jobs_applied.append(JobApplication(user_id=user.id, job_id=job.id))

    db.session.add(user)

    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': "Applied successfully"
    })


@jobs_blueprint.route('/post/', methods=['POST'])
@validate_auth_token
def post_job():
    # todo validate data types passed.
    rjson = request.json

    if rjson is None:
        return jsonify({
            'status': 'error',
            'message': "No data provided"
        }), 400

    user_id = decode_auth_token(get_auth_token(request))['sub']

    user = User.query.filter_by(id=user_id).first()

    if user is None:
        # this should not ever happen but if it does.
        return jsonify({
            'status': 'error',
            'message': "Unable to validate user"
        }), 401

    title = rjson.get('title')
    description = rjson.get('description')
    longitude = str(rjson.get('longitude'))
    latitude = str(rjson.get('latitude'))

    job_type = rjson.get('job_type')
    category = rjson.get('category')

    invalid_fields = []

    _category = None

    _job_type = None

    if isBlank(title):
        invalid_fields.append('title')

    if isBlank(description):
        invalid_fields.append('description')

    if isBlank(longitude):
        invalid_fields.append('longitude')

    if isBlank(latitude):
        invalid_fields.append('latitude')

    if not isBlank(job_type):
        _job_type = JobType.query.filter_by(name=job_type).first()

        if _job_type is None:
            invalid_fields.append('job_type')

    if not isBlank(category):
        _category = JobCategory.query.filter_by(name=category).first()

        if _category is None:
            invalid_fields.append('category')

    if len(invalid_fields) > 0:

        payload = {}

        for invalid_field in invalid_fields:
            payload[invalid_field] = rjson.get(invalid_field)

        return jsonify({
            'status': 'error',
            'message': 'Invalid Field Input',
            'payload': payload
        }), 400

    # todo validate response input.

    # todo check if there's a listing at the given lat / long location?

    if _category is None or _job_type is None:
        return jsonify({
            'status': 'error',
            'message': 'No category or job type provided when posting job.',
            'payload': {
                'category': category,
                'job_type': job_type
            }
        })

    job = Job(owner_id=user.id, title=title, description=description, longitude=longitude, latitude=latitude,
              category_id=_category.id, job_type_id=_job_type.id,category=_category,job_type=_job_type)

    db.session.add(job)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Job listing posted',
        'job': job.to_dict()
    })


@jobs_blueprint.route('/info/<int:id>', methods=['GET'])
@validate_auth_token
def get_job_info(id):
    if id is None:
        return jsonify({
            'status': 'error',
            'message': "Invalid Job ID"
        }), 400

    job = Job.query.filter_by(id=id).first()

    user = get_user(request)

    if job is None:
        return jsonify({
            'status': 'error',
            'message': 'Invalid Job ID'
        }), 400

    job_info = job.to_dict()

    if not job.is_owner(user):
        job_info['applied'] = job.has_applied(user)

    return jsonify({
        'status': 'success',
        'message': '',
        'job': job_info
    })


@jobs_blueprint.route('/list', methods=['GET'])
@jobs_blueprint.route('/list/<filter>', methods=['GET'])
def list_jobs(filter="all"):
    jobs_info = []
    jobs = Job.query.all()

    if not is_validated_user_request(request):
        if len(jobs) > 0:
            for job in jobs:
                jobs_info.append(job.to_dict())
    else:
        user = get_user(request)

        if filter == "applied":
            if len(user.jobs_applied) > 0:
                for job_app in user.jobs_applied:
                    job = job_app.job

                    ji = job.to_dict()

                    if not job.is_owner(user):
                        ji['applied'] = job.has_applied(user)

                    jobs_info.append(ji)

            return jsonify({
                'status': 'success',
                'message': '',
                'jobs': jobs_info
            })

        if len(jobs) > 0:
            for job in jobs:
                ji = job.to_dict()
                if not job.is_owner(user):
                    ji['applied'] = job.has_applied(user)
                jobs_info.append(ji)

    return jsonify({
        'status': "success",
        'message': "",
        'jobs': jobs_info
    }), 200
