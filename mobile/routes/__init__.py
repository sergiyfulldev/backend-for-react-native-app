from mobile.routes.auth import auth as authentication_blueprint
from mobile.routes.jobs import jobs_blueprint
from mobile.routes.user import user_blueprint
from mobile.routes.index import index_blueprint

# ========== Administrative Routes =============

from mobile.routes.admin import admin_users_blueprint, admin_permissions_blueprint