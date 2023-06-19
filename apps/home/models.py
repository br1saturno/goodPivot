from apps import db


class AText(db.Model):

    __tablename__ = "user_smarts"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(250), nullable=False)
    prompt = db.Column(db.String(1000), nullable=False)
    response = db.Column(db.String(10000), nullable=False)
    total_tokens = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    delta = db.Column(db.Float, nullable=False)
