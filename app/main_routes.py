from flask import Blueprint,render_template,request,redirect,url_for,flash
from .models import Store
from flask_login import login_required,current_user
# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    )



"""Route for handling 404 errors """
@main_bp.app_errorhandler(404)
def e404(e):


    return render_template("e404.html")

"""Route for handling and displaying any kind of errors  """
@main_bp.route("/error/<msg>",)
def error(msg):

    return render_template("error.html",msg=msg)
