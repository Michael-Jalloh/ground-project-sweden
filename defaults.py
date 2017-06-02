from flask import Blueprint, render_template
from flask.views import MethodView
from flask_login import current_user
from playhouse.flask_utils import get_object_or_404
from models import Post, User

defaults = Blueprint('defaults',__name__, template_folder='templates')

class HomeView(MethodView):
	def get(self):
		try:
			post = Post.get(Post.title=='Home')
		except:
			post = None
		try:
			if current_user.role == 'admin':
				return render_template('posts/admin_defaults.html',post=post, title='Home')
		except:
			pass
		return render_template('posts/defaults.html', post=post, title='Home')

class VisionView(MethodView):
	def get(self):
		try:
			post = Post.get(Post.title=='Vision')
		except:
			post = None
		try:
			if current_user.role=='admin':
				return render_template('posts/admin_defaults.html',post=post, title='Vision')
		except:
			pass
		return render_template('posts/defaults.html',post=post, title='Vision')


class AboutView(MethodView):
	def get(self):
		users = User.select().where(User.role=='admin')
		try:
			post = Post.get(Post.title=='About')
		except:
			post= None
		try:
			if current_user.role =='admin':
				return render_template('posts/admin_about.html',post=post, title='About', users=users)
		except:
			pass
		return render_template('posts/about.html',post=post, title='About', users=users)

class MissionView(MethodView):
	def get(self):
		try:
			post = Post.get(Post.title=='Mission')
		except:
			post = None
		try:
			if current_user.role == 'admin':
				return render_template('posts/admin_defaults.html',post=post, title='Mission')
		except:
			pass
		return render_template('posts/defaults.html',post=post, title='Mission')

defaults.add_url_rule('/', view_func=HomeView.as_view('/'))
defaults.add_url_rule('/home/',view_func=HomeView.as_view('home'))
defaults.add_url_rule('/vision/',view_func=VisionView.as_view('vision'))
defaults.add_url_rule('/about/',view_func=AboutView.as_view('about'))
defaults.add_url_rule('/mission/', view_func=MissionView.as_view('mission'))
