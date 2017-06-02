from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask.views import MethodView
from flask_login import current_user, login_required
from models import Comment
from app import admin_permission


forum = Blueprint('forum', __name__, template_folder='templates')

class ForumView(MethodView):
	def get(self):
		try:
			comments = Comment.select()
		except:
			comments = None
		return render_template('forum.html', comments=comments)

	def post(self):
		next_url = request.args.get('next')
		print next_url
		comment = Comment()
		if current_user.is_authenticated:
			comment.author = current_user.id
			comment.content = request.form.get('content')
			comment.save()
			flash('Comment saved', 'success')
		else:
			flash('Please Login or Signin to add a comment','dnager')
			return redirect(url_for('auth.login', next_url=next_url))
		return redirect(url_for('forum.forum'))

class DeleteComment(MethodView):
	def get(self,comment_id):
		comment = Comment.get(Comment.id == comment_id)
		comment.delete_instance()
		flash('Comment deleted','success')
		return redirect(url_for('forum.forum'))

# Register urls
forum.add_url_rule('/forum/', view_func=ForumView.as_view('forum'))
forum.add_url_rule('/forum/delete/<comment_id>',view_func=DeleteComment.as_view('delete'))
