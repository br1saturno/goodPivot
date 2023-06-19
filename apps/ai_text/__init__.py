from flask import Blueprint

aitext_bp = Blueprint('aitext', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/assets')

# from . import routes