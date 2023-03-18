from utils import db


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False, unique=True)
    courses = db.relationship('Course', backref='students', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)

    def __repr__(self):
        return f"Student(email='{self.email}')"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def delete_by_id(cls, id):
        model = cls.query.get(id)
        if not model:
            return False
        db.session.delete(model)
        db.session.commit()
        return True
