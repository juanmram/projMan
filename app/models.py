from app import db
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  department = db.Column(db.String(128))
  role = db.Column(db.String(128))

  def __init__(self, name, department, role):
        self.name = name
        self.department = department
        self.role = role

