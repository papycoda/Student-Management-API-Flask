from utils import db


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return f"Grade(score={self.score})"

    def save(self):
        db.session.add(self)
        db.session.commit()
