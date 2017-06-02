from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import login_required, current_user
from playhouse.flask_utils import get_object_or_404
from models import Post, Comment, PostIndex
from app import admin_permission

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
	decorators = [login_required,  admin_permission.require(http_exception=403)]

	def get(self):
		posts = Post.select()
		return render_template('admin/list.html', posts=posts)


class Create(MethodView):
	decorators = [login_required, admin_permission.require(http_exception=403)]

	def get(self):
		return render_template('admin/create.html')

	def post(self):
		post = Post()
		post.title = request.form.get('title')
		post.content = request.form.get('content')
		post.publihed = request.form.get('published') or False
		post.author = int(current_user.id)
		post.save()
		return redirect(url_for('posts.detail', slug=post.slug))


class Edit(MethodView):
	decorators = [login_required, admin_permission.require(http_exception=403)]
	def get(self, slug):
		post = Post.get(Post.slug == slug)
		return render_template('admin/edit.html', post=post)

	def post(self, slug):
		post = Post.get(Post.slug == slug)
		post.title = request.form.get('title')
		post.content = request.form.get('content')
		post.published = request.form.get('published') or False
		post.author = int(current_user.id)
		post.save()
		return redirect(url_for('posts.detail', slug=post.slug))

class Delete(MethodView):
	decorators = [login_required, admin_permission.require(http_exception=403)]
	def get(self,slug):
		query = Post.select()
		post = get_object_or_404(query,Post.slug==slug)
		post.delete_instance()
		return redirect('/admin/')
		


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', view_func=Create.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Edit.as_view('edit'))
admin.add_url_rule('/admin/delete/<slug>/', view_func=Delete.as_view('delete'))
