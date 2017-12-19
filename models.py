from google.appengine.ext import ndb





class ITM(ndb.Model):
    teza = ndb.IntegerProperty()
    visina = ndb.IntegerProperty()
    spol = ndb.StringProperty()



class Komentar(ndb.Model):
    ime = ndb.StringProperty()
    komentar = ndb.StringProperty()
    cas_vnosa = ndb.DateTimeProperty(auto_now_add=True)



