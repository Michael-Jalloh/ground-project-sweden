from flask import Flask, render_template, Markup, flash, redirect, url_for
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed, UserNeed, ActionNeed
from markdown import markdown

application = Flask(__name__)
application.config.from_object('config')
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view= 'auth.login'

# Needa
be_admin = RoleNeed('admin')
be_user = ActionNeed('user')

# Permissiona
user_permission = Permission(be_user)
user_permission.description = "User's permissins"
admin_permission = Permission(be_admin)
admin_permission.description = "Admin's permissions"

apps_needs = [be_admin, be_user]
apps_permissions = [user_permission, admin_permission]

def register_blueprint(app):
	# Prevent circular imprts
	from auth import auth
	from views import posts
	from admin import admin
	from defaults import defaults
	from forum import forum
	from profile import profile
	app.register_blueprint(auth)
	app.register_blueprint(posts)
	app.register_blueprint(admin)
	app.register_blueprint(defaults)
	app.register_blueprint(forum)
	app.register_blueprint(profile)
	login_manager.init_app(app)
	Principal(app)



	@application.errorhandler(403)
	def forbidden(e):
		return redirect(url_for('defaults.home'))

	@application.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html')

	@application.errorhandler(500)
	def internal_error(e):
		return render_template('500.html')
register_blueprint(application)

if __name__ == '__main__':
	application.run(debug=True,host='0.0.0.0')
