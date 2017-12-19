#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users
from models import ITM
import time
from models import Komentar


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("homepage.html")


class ItmHandler(BaseHandler):
    def get(self):
        return self.render_template("itm.html")

    def post(self):
        visina_v_cm = self.request.get("visina")
        teza = self.request.get("teza")
        spol = self.request.get("spol")

        visina_v_m = float(int(visina_v_cm)) / 100
        teza = float(teza)
        visina = visina_v_m * visina_v_m
        itm = teza / visina

        params = {"itm": itm}

        return self.render_template("itm_rezultat.html", params=params)


class KomentarHandler(BaseHandler):
    def get(self):
        return self.render_template("komentar_treninga.html")

    def post(self):
        ime = self.request.get("ime")
        komentar = self.request.get("komentar")

        sporocilo = Komentar(ime=ime, komentar=komentar)
        sporocilo.put()

        return self.write("Komentiral sem:" + komentar)

class VsiKomentarjiHandler(BaseHandler):
    def get(self):
        sporocila = Sporocilo.query().fetch()
        params = {"seznam": sporocila}

        return self.render_template("vsi_komentarji.html", params=params)







app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/itm", ItmHandler),
    webapp2.Route("/komentar", KomentarHandler),
    webapp2.Route("/vsikomentarji", VsiKomentarjiHandler),
], debug=True)
