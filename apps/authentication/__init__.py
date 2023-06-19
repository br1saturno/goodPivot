from flask import Blueprint

auth_bp = Blueprint('authentication', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/assets')

# from . import routes