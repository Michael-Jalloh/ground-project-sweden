from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from playhouse.flask_utils import get_object_or_404
from models import Post, Comment, PostIndex
from flask_login import login_required, current_user
from app import admin_permission
#from config import POST_PER_PAGE
ppp = 5


posts = Blueprint('posts',__name__, template_folder='templates')
POST_PER_PAGE = 5

                
class ListView(MethodView):

	def get(self,page=1):
		search_query = request.args.get('q')
		if search_query:
			posts = Post.search(search_query)
			max_page = PostIndex.max_post_page_all(search_query)
		else:
			max_page = Post.max_post_page_all()
			posts = Post.select().where(Post.published==True).order_by(Post.timestamp.desc()).paginate(page,POST_PER_PAGE)
		return render_template('posts/list.html', posts=posts, page=page, max_page= max_page)


class DetailView(MethodView):


	
	def get(self, slug):
		try:
			post = Post.get(Post.slug==slug)
		except:
			post= None
		try:
			if current_user.role == 'admin':
				return render_template('posts/admin_detail.html', post=post, title=post.title)
		except:
			pass
		return render_template('posts/detail.html', post=post, title=post.title)


class CommentDelete(MethodView):
	decorators=[login_required, admin_permission.require(http_exception=403)]
	
	def get(self,comment, slug):
		comment = Comment.get(id=int(comment))
		comment.delete_instance()
		
		return redirect(url_for('posts.detail', slug=slug))


# Register the urls
posts.add_url_rule('/projects/', view_func=ListView.as_view('projects'))
posts.add_url_rule('/<int:page>/', view_func=ListView.as_view('page'))
posts.add_url_rule('/project/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/comment/delete/<slug>/<comment>/', view_func=CommentDelete.as_view('delete'))
