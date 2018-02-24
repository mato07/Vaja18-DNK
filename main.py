#!/usr/bin/env python
import os
import jinja2
import webapp2


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

class DNKAnaliza:
    def __init__(self, DNKstring):
        self.DNKstring = DNKstring

    def barva_las(self):
        if "CCAGCAATCGC" in self.DNKstring:
            return "crna"
        elif "GCCAGTGCCG" in self.DNKstring:
            return "rjava"
        elif "TTAGCTATCGC" in self.DNKstring:
            return "korencek"
        else:
            return "nedefinirana"

    def oblika_obraza(self):
        if "GCCACGG" in self.DNKstring:
            return "kvadraten"
        elif "ACCACAA" in self.DNKstring:
            return "okrogel"
        elif "AGGCCTCA" in self.DNKstring:
            return "ovalen"
        else:
            return "nedefiniran"

    def barva_oci(self):
        if "TTGTGGTGGC" in self.DNKstring:
            return "modra"
        elif "GGGAGGTGGC" in self.DNKstring:
            return "zelena"
        elif "AAGTAGTGAC" in self.DNKstring:
            return "rjava"
        else:
            return "nedefiniran"

    def spol(self):
        if "TGCAGGAACTTC" in self.DNKstring:
            return "moski"
        elif "TGAAGGACCTTC" in self.DNKstring:
            return "zenska"
        else:
            return "nedefiniran"

    def rasa(self):
        if "AAAACCTCA" in self.DNKstring:
            return "belec"
        elif "CGACTACAG" in self.DNKstring:
            return "crnec"
        elif "CGCGGGCCG" in self.DNKstring:
            return "azijec"
        else:
            return "nedefeniran"

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")

class ResultHandler(BaseHandler):
    def post(self):

        DNK = DNKAnaliza(self.request.get("DNKosebe"))
        barvalas = DNK.barva_las()
        oblikaobraza = DNK.oblika_obraza()
        barvaoci = DNK.barva_oci()
        spoll = DNK.spol()
        rasaa = DNK.rasa()

        podatki = {"alasje": barvalas,
                   "aobraz": oblikaobraza,
                   "aoci": barvaoci,
                   "aspol": spoll,
                   "arasa": rasaa}

        return self.render_template("result.html", podatki)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler)

], debug=True)
