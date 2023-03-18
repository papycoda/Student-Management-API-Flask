from utils import db


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    type_acct = db.Column(db.String(5), nullable=False)

    def __str__(self):
        return f"Admin('{self.email}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
