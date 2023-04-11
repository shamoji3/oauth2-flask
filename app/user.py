from flask_login import UserMixin

class User(UserMixin):

  uid     = ""
  name    = ""
  email   = ""
  picture = ""

  def get_id(self):
    return self.uid

  @classmethod
  def instaniate(cls, uid:str, name:str, email:str, picture:str):
    instance = cls()
    instance.uid     = uid
    instance.name    = name
    instance.email   = email
    instance.picture = picture
    return instance