from mobile.database import db, SqlModel
import datetime



user_permissions = db.Table('user_permission',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                            db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
                            )


class JobCategory(SqlModel):
    __tablename__ = "job_category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def to_dict(self):

        job_types = []

        for _type in self.job_types:
            job_types.append(_type.to_dict())

        return dict(
            id=self.id,
            name=self.name,
            job_types=job_types
        )


class JobType(SqlModel):
    __tablename__ = "job_type"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    category = db.relationship('JobCategory',backref=db.backref('job_types',cascade='all, delete'),lazy=True,uselist=False)
    category_id = db.Column(db.Integer, db.ForeignKey('job_category.id'),nullable=False)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            category=dict(
                id=self.category_id,
                name=self.category.name
            )
        )


class Permission(SqlModel):
    """
    Model for the object which describes a users permissions.

    Refer to #### todo fill with annotation link
    """
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name
        )


class UserJobExperience(SqlModel):
    __tablename__ = "user_job_experience"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False,primary_key=True)
    job_category_id = db.Column(db.Integer, db.ForeignKey('job_category.id'), nullable=False, primary_key=True)

    job_category = db.relationship('JobCategory',backref=db.backref('users_with_experience',cascade='all, delete-orphan'),lazy=True)

    years_experience = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return dict(
            user_id=self.user_id,
            job_category_id=self.job_category_id,
            job_category=self.job_category.name,
            years_experience = self.years_experience
        )

class UserSkills(SqlModel):
    __tablename__ = "user_skills"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False,primary_key=True)
    name = db.Column(db.Text)

    def to_dict(self):
        return dict(
            user_id=self.user_id,
            name=self.name
        )

class User(SqlModel):
    __tablename__ = "user"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)

    about = db.Column(db.Text)

    verified = db.Column(db.Boolean, default=False)

    jobs_posted = db.relationship("Job", backref="owner", lazy=True)

    jobs_applied = db.relationship("JobApplication", backref="user", lazy=True, cascade="all,delete")

    permissions = db.relationship('Permission', secondary=user_permissions, backref=db.backref('users', lazy=True),
                                  lazy="subquery")

    job_experience = db.relationship("UserJobExperience", backref=db.backref('user',cascade='all, delete',uselist=False),lazy=True)

    skills = db.relationship('UserSkills',backref=db.backref('user',cascade='all, delete',uselist=False),lazy=True)

    def to_dict(self):
        jobs_posted = []

        jobs_applied = []

        permissions = []

        job_experience = []

        skills = []

        if len(self.jobs_posted) > 0:
            for _jbp in self.jobs_posted:
                jobs_posted.append(_jbp.to_dict())

        if len(self.jobs_applied) > 0:
            for _jba in self.jobs_applied:
                jobs_applied.append(_jba.to_dict())

        if len(self.permissions) > 0:
            for _perm in self.permissions:
                permissions.append(_perm.to_dict())

        if len(self.job_experience) > 0:
            for job_with_experience in self.job_experience:
                job_experience.append(job_with_experience.to_dict())

        if len(self.skills) > 0:
            for skill in self.skills:
                skills.append(skill.to_dict())

        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
            about=self.about,
            jobs_posted=jobs_posted,
            jobs_applied=jobs_applied,
            permissions=permissions,
            experience=job_experience,
            skills=skills
        )

class Job(SqlModel):
    __tablename = "job"
    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    title = db.Column(db.Text, nullable=False)

    description = db.Column(db.Text, nullable=False)

    longitude = db.Column(db.Text, nullable=False)

    latitude = db.Column(db.Text, nullable=False)

    category = db.relationship('JobCategory', backref=db.backref('jobs',cascade="all, delete"), lazy=True, uselist=False)

    job_type = db.relationship('JobType', backref=db.backref('jobs', cascade="all, delete"), lazy=True, uselist=False)

    job_type_id = db.Column(db.Integer, db.ForeignKey('job_type.id'))

    category_id = db.Column(db.Integer, db.ForeignKey('job_category.id'))

    def is_owner(self, user):
        return self.owner_id == user.id

    def has_applied(self, user):
        job_application = JobApplication.query.filter_by(user_id=user.id, job_id=self.id).first()
        return job_application is not None

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'title': self.title,
            'description': self.description,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'category': self.category.name,
            'job_type': self.job_type.name,
            'category_id': self.category_id,
            'job_type_id': self.job_type_id
        }


class JobApplication(SqlModel):
    __tablename__ = "job_application"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    job = db.relationship('Job', backref="applications", cascade="all, delete", lazy=True)

    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def to_dict(self):
        return dict(
            job=self.job.to_dict(),
            date_submitted=self.date_submitted.strftime("%Y-%m-%d %H:%M:%S")
        )
