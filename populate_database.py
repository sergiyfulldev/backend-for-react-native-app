from mobile.factory import create_application
from mobile.extensions import db
from mobile.models import JobCategory, JobType

application = create_application()

job_type_categories = {
    'Restaurant': [
        'Barista',
        'Chef',
        'Server',
        'Dish Washing / Cleaning',
        'Bartending'
    ],
    'Retail': [
        'Cashier',
        'Customer Service'
    ],
    'Transportation': [
        'Driver',
        'Delivery',
        'Car Pool'
    ],
    'Cleaner': [
        'Domestic Cleaning',
        'Cabin Cleaning',
    ],
    'House Keeper': [
        'House Sitting',
        'House Cleaning'
    ],
    'Child Care': [
        'Babysitting'
    ],
    'Pet Care': [
        'Dog Walking',
        'Pet Sitting',
        'Pet Lodging'
    ],
    'Office Admin': [
        'Receptionist',
        'Office Assistant',
        'Office Manager'
    ],
    'Tutoring': [
        'French Tutoring',
        'English Tutoring',
    ],
    'Labour': [
        'General Labour',
    ],
    'IT': [
        'Graphic Designer',
        'Developer',
        'Support / QA'
    ]
}


if __name__ == "__main__":

    try:
        print("Creating database, please wait.")
        db.create_all(app=application)
    except:
        print("Database exists; Operation resumed")

    # With so we have the app context.
    with application.app_context():
        # Query database first and see if the items exist
        # if the database is populated with items, exit script
        # otherwise insert the default values.

        for key,value in job_type_categories.items():
            category = JobCategory.query.filter_by(name=key).first()

            if category is None:
                category = JobCategory(name=key)
                category.save(commit=True)
            else:
                print("! Category {0} ALREADY EXISTS".format(key))

            # Iterate value as its a list
            for job_type in value:
                _type = JobType.query.filter_by(name=job_type).first()

                if _type is None:
                    _type = JobType(name=job_type,category=category)
                    _type.save(commit=True)
                    print("+ {0} in {1}".format(_type.name,category.name))
