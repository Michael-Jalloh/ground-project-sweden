from peewee import *
import re
import datetime
from hashlib import md5
from flask import Markup
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from playhouse.sqlite_ext import *
from app import login_manager

database = SqliteDatabase('GPS.db')

ppp = 5

class BaseModel(Model):
	class Meta:
		database = database


class User(UserMixin, BaseModel):
	email = CharField(unique=True, default='')
	username = CharField()
	password_hash = CharField()
	pic = CharField(default='')
	role = CharField(default='user')
	about_me = TextField(default='')

	def avatar(self, size):
				return 'https://secure.gravatar.com/avatar/%s?d=identicon&s=%d' %( md5(self.email.encode('utf-8')).hexdigest(), size)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@property
	def photo(self,size=20):
		if self.pic:
			img = '/' + self.pic
		else:
			img = self.avatar(size)
		return img


	@property
	def html_content(self):

	# This function will be use to turn our post content into html
		hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
		extras = ExtraExtension()
		content = self.converter()
		markdown_content = markdown(content, extensions=[hilite, extras])
		#       oembed_content = parse_html(
		#               markdown_content,
				#       oembed_providers,
		#               urlize_all=True,
		#               maxwidth=SITE_WIDTH)

		return Markup(markdown_content)


	def converter(self):
                conv = ''
		content = self.about_me
		while 1:
        		try:
                        	if '<pre>' in content:
                                        first, rest = content.split('<pre>',1)
					code, content = rest.split('</pre>',1)
					conv = conv+first.replace('\n','<br>')+'<pre>'+code+'</pre>'
				else:
					conv = conv + content.replace('\n','<br>')
					break
			except:
				break
		return conv


	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


	@login_manager.user_loader
	def load_user(user_id):
		return User.get(User.id == int(user_id))

class Post(BaseModel):
	title = CharField()
	slug = CharField(unique=True)
	post_type = CharField(default = '')
	published = BooleanField(default=False,index=True)
	timestamp = DateTimeField(default=datetime.datetime.now, index=True)
	content = TextField()
	author = ForeignKeyField(User, related_name='posts')

	def save(self, *args, **kwargs):
		self.slug = re.sub('[^\w]+', '-', self.title.lower())
		ret = super(Post, self).save(*args, **kwargs)

		# Store search content
		return ret


	def converter(self):
		conv = ''
		content = self.content
		while 1:
			try:
				if '<pre>' in content:
					first, rest = content.split('<pre>',1)
					code, content = rest.split('</pre>',1)
					conv = conv+first.replace('\n','<br>')+'<pre>'+code+'</pre>'
				else:
					conv = conv + content.replace('\n','<br>')
					break
			except:
				break
		return conv

	@classmethod
	def max_post_page_all(self):
		m = float(Post.select().count())/ ppp
		n = Post.select().count()/ ppp
		if m>n:
			n = n +1
		return n

	@classmethod
	def max_post_page_public(self):
		m = float(Post.public().count())/ ppp
		n = Post.public().count() / ppp
		if m>n:
			n = n + 1
		return n


	@property
	def html_content(self):
	# This function will be use to turn our post content into html
		hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
		extras = ExtraExtension()
		content = self.converter()
		markdown_content = markdown(content, extensions=[hilite, extras])
	#	oembed_content = parse_html(
	#		markdown_content,
		#	oembed_providers,
	#		urlize_all=True,
	#		maxwidth=SITE_WIDTH)

		return Markup(markdown_content)





	@classmethod
	def public(cls):
		query = Post.select().where(Post.published == True)



	@classmethod
	def private(cls):
		return Post.select().where(Post.published == False)


	@classmethod
	def search(cls, query):
		words = [word.strip() for word in query.split() if word.strip()]
		if not words:
			# Return empty query.
			return Post.select().where(Post.id == 0)
		else:
			ids = []
			posts = []
			for word in words:
				indexes = PostIndex.search(word)
				for post_search in indexes:
					if post_search.post_id in ids or post_search.post_id == None:
						pass
					else:
						ids.append(post_search.post_id)
						posts.append(Post.get(id=post_search.post_id))

		return posts


class PostIndex(FTSModel):
	post_id = IntegerField()
	content = TextField()
	published = BooleanField()

        class Meta:
                database = database


	@classmethod
	def max_post_page_all(cls,query):
		m = float(PostIndex.search(query).count()) / ppp
		n = PostIndex.search(query).count() / ppp
		if m > n:
			n = n + 1
		return n

	@classmethod
	def max_post_page_public(cls, query):
		m = float(PostIndex.search(query).where(PostIndex.published==True).count()) / ppp
		n = PostIndex.search(query).where(PostIndex.published==True).count() / ppp
		if m > n:
			n = n + 1
		return n



	class Meta:
		database = database

class ProductIndex(FTSModel):
	product_id = IntegerField()
	content = TextField()

	@classmethod
	def max_product_page_all(cs, query):
		m = float(ProductIndex.search(query).count()) / ppp
		n = ProductIndex.search(query).count() / ppp
		if m > n:
			n = n + 1
		return n

class Comment(BaseModel):
	timestamp = DateTimeField(default=datetime.datetime.now, index=True)
	content = TextField()
	author = ForeignKeyField(User, related_name='comments', default='')

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' %( md5(self.email.encode('utf-8')).hexdigest(), size)


class Product(Model):
	name = CharField()
	description = TextField(default='')
	price = CharField()
	old_price = CharField(default='')
	slug = CharField(unique=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = re.sub('[^\w]+','-', self,name.lower())
		ret = super(Product, self).save(*args, **kwargs)
		return ret



	def converter(self):
		conv = ''
		content = self.description
		while 1:
			try:
				if '<pre>' in content:
					first, rest = content.split('<pre>',1)
					code, content = rest.split('</pre>',1)
					conv = conv+first.replace('\n', '<br>') + '<pre>'+code+'</pre>'
				else:
					conv = conv+ content.replace('\n','<br>')
			except:
				break
		return conv


	@property
	def html_content(self):
		'''
		Generate HTML representation of the markdown-formatted blog entry,
		and also convert any media URLs into rich media objects uch as video
		players or images
		'''
		hilite = CodeHiliteExtension(linenums=True, css_class='highlight')
		extras = ExtraExtension()
		content = self.converter()
		markdown_content = markdown(content, extension=[hilite, extras])
		'''
		oembed_content = parse_html(
			markdown_content,
			oembed_providers,
			urlize_all=True,
			maxwidth=800)
		return Markup(iembed_content)
		'''
		return Markup(markdown_content)

	@classmethod
	def max_product_per_page(self):
		m = float(Product.select().count())/ ppp
		n = Product.select().count() / ppp
		if m > n:
			n = n + 1
		return n



database.create_tables([ User, Post, Comment], safe=True)
