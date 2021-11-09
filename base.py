from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_url = db.Column(db.String(60), unique=False, nullable=False)
    page_view_count = db.Column(db.Integer, unique=False, nullable=False)
    last_seen = db.Column(db.String(60), unique=False, nullable=False)
    timestamp = db.Column(db.PickleType, unique=False, nullable=False)
    
    def __init__(self, id, page_url, page_view_count, last_seen, timestamp):
        self.id = id
        self.page_url = page_url
        self.page_view_count = page_view_count
        self.last_seen = last_seen
        self.timestamp = timestamp
        
    def json(self):
        return {'id':self.id, 'page_url': self.page_url, 'page_view_count': self.page_view_count, 'last_seen': self.last_seen, 'timestamp': self.timestamp}
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def save_to(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
