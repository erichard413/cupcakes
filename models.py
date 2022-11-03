"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




default_img = 'https://tinyurl.com/demo-cupcake'

class Cupcake(db.Model):
    """Cupcake model"""
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=default_img)
    
    def to_dict(self):
        """Serialize cupcake"""
        return {"id": self.id, "flavor": self.flavor, "rating": self.rating, "size": self.size, "image": self.image}
    
    def __repr__(self):
        """Representation output"""
        return f"<Cupcake {self.id} {self.flavor} {self.size} {self.rating} {self.image}>"
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)