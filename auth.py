from flask import Blueprint, g, request, redirect, render_template, url_for, flash, session, current_app
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required
from flask_principal import Identity, identity_changed, identity_loaded, AnonymousIdentity
from models import User
from app import be_user, be_admin

auth = Blueprint('auth',__name__, template_folder='templates')


@identity_loaded.connect
def on_identity_loaded(sender, identity):
	needs = []

    	if identity.id in ('user', 'admin'):
        	needs.append(be_user)

    	if identity.id == 'admin':
        	needs.append(be_admin)



    	for n in needs:
        	g.identity.provides.add(n)


class Login(MethodView):

	def get(self):
		next_url = request.args.get('next')
		return render_template('auth/login.html')


	def post(self):
		next_url = request.args.get('next')
		try:
			email = request.form.get('email')	
			password = request.form.get('password')
			remember_me = request.form.get('remember_me')
			user = User.get(User.email == email)
			if user is not None and user.verify_password(password):
				login_user(user, remember_me)
				flash('Login Successful','success')
				identity_changed.send(current_app._get_current_object(), identity=Identity(user.role))
				
				return redirect(next_url or 'admin')
		except User.DoesNotExist:
			flash("Either user doesn't exist or password wrong")
			redirect('login')
		return render_template('auth/login.html')

class Signup(MethodView):
	def get(self):
		return render_template('auth/login.html')

	
	def post(self):
		email = request.form.get('email')
		name = request.form.get('name')
		pass1 = request.form.get('password1')
		pass2 = request.form.get('password2')
		if pass1 == pass2:
			user = User()
			user.email = email
			user.username = name
			user.password = pass1
			user.save()
			flash('User successfully created', 'success')
			login_user(user)
			return redirect('/')
		else:
			flash('Password Do not match', 'danger')
		return render_template('auth/login.html')

class Logout(MethodView):
	decorators = [login_required]
	def get(e):
		for key in ['identity.id','identity.auth_type']:
			session.pop(key, None)
		logout_user()
		identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
		return redirect('/')


# Regiter the url
auth.add_url_rule('/login/', view_func=Login.as_view('login'))
auth.add_url_rule('/signup/', view_func=Signup.as_view('signup'))
auth.add_url_rule('/logout/', view_func=Logout.as_view('logout'))
