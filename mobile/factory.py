from flask import Flask

from mobile.config import BaseConfig

def create_application(config_override=None):
    """
    Create an instance of the application, and optionally provide a config object for settings override.
    :param config_override: settings to provide to the application.
    :return: instance of a configured flask application
    """

    app = Flask(__name__)
    configure_application(app, BaseConfig if config_override is None else config_override)

    register_blueprints(app)

    register_extensions(app)

    return app



def configure_application(app, config):
    """
    Apply specific application config here.
    :param app: application to apply the configuration to
    """
    app.config.from_object(config)


def register_blueprints(app):
    """
    Register blueprints that the application will be using.
    """

    from mobile.routes import jobs_blueprint, authentication_blueprint, user_blueprint, index_blueprint

    # ENDPOINTS USED BY USERS
    app.register_blueprint(jobs_blueprint,url_prefix="/api/jobs")
    app.register_blueprint(authentication_blueprint, url_prefix='/api/auth')
    app.register_blueprint(user_blueprint,url_prefix='/api/users')
    app.register_blueprint(index_blueprint,url_prefix="/")

    # ENDPOINTS THAT ARE ACCESSED VIA THE DASHBOARD / ADMIN

    from mobile.routes import admin_users_blueprint, admin_permissions_blueprint
    app.register_blueprint(admin_users_blueprint,url_prefix='/api/admin/users')
    app.register_blueprint(admin_permissions_blueprint,url_prefix='/api/admin/permissions')


def register_extensions(app):
    """
    Register the extensions for the application
    """

    from mobile.extensions import db, bcrypt, mail, cors, migrate

    db.init_app(app)

    migrate.init_app(app=app,db=db)

    import mobile.models

    bcrypt.init_app(app)

    mail.init_app(app)

    cors.init_app(app)