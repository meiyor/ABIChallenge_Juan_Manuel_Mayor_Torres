from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True, index=True)
    code = db.Column(db.String)
    date = db.Column(db.String)
    username = db.Column(db.String)
    Interaction_Register = db.Column(db.PickleType)
    Images_Files = db.Column(db.PickleType)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'<chatbot {self.firstname}>'
