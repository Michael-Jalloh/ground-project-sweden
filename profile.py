from flask import Blueprint, request, render_template, url_for, flash, redirect
from flask.views import MethodView
from models import User
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import admin_permission


profile = Blueprint('profile', __name__, template_folder='templates')
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg','jpeg'])

def allow_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
class ProfileView(MethodView):
    def get(self,user_id):
        user = User.get(User.id == int(user_id))
        return render_template('profile/detail.html', user=user)


class ProfileEdit(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('profile/user.html')

    def post(self):
        user = User.get(User.id==current_user.id)
        user.email = request.form.get('email')
        user.username = request.form.get('username')
        user.about_me = request.form.get('about_me')
        user.save()
        flash('Profile Updated', 'success')
        return redirect(url_for('profile.info', user_id=user.id))


class PhotoUpload(MethodView):
    decorators=[login_required]

    def get(self):
        return redirect(url_for('profile.info', user_id=current_user.id))

    def post(self):
        if 'file' not in request.files:
            flash('No file')
            return redirect(url_for('profile.info',user_id=current_user.id))
        file = request.files['file']
        if file.filename =='':
            flash('No selected file')
            return redirect(url_for('profile.info', user_id=current_user.id))
        if file and allow_file(file.filename):
            user = User.get(User.id==current_user.id)
            filename = secure_filename(str(user.id)+user.username+file.filename)
            file.save(os.path.join(UPLOAD_FOLDER,filename))

            user.pic = os.path.join(UPLOAD_FOLDER,filename)
            user.save()
            flash('Profile picture updated', 'success')
            return redirect(url_for('profile.info', user_id=current_user.id))
        flash('Something went wrong', 'danger')
        return url_for('profile.info', user_id=current_user.id
        )
# Registe the urls
profile.add_url_rule('/profile/<user_id>', view_func=ProfileView.as_view('info'))
profile.add_url_rule('/profile/edit/', view_func=ProfileEdit.as_view('edit'))
profile.add_url_rule('/profile/picture/', view_func=PhotoUpload.as_view('photo'))
