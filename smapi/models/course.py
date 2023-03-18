from utils import db

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    instructor = db.Column(db.String(30), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))
    student = db.relationship('Student', backref='courses')

    def __repr__(self):
        return f"Course('{self.name}')"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def delete_student_course(cls, id):
        model = cls.query.get(id)
        if not model:
            return False
        db.session.delete(model)
        db.session.commit()
        return True
