#!/usr/bin/env python
#


import webapp2
import os
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
																autoescape=True)

class Art(db.Model):
	title = db.StringProperty(required=True)
	art = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kwArgs):
		self.response.write(*a, **kwArgs)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def renderIt(self, template, **kwArgs):
		self.write(self.render_str(template, **kwArgs))


class MainHandler(Handler):
	def render_front(self, title="", art="", error=""):
		arts = db.GqlQuery("SELECT * FROM Art" 
							" ORDER BY created DESC")

		self.renderIt("front.html", title=title, art=art, error=error, arts=arts)


	def get(self):
		self.render_front()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if art and title:
			a = Art(title = title, art = art)
			a.put()

			self.redirect("/")
		else:
			error = "we need both a title and some artwork!"
			self.render_front(title, art, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
