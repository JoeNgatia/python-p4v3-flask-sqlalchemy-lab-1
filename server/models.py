from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Earthquake(db.Model, SerializerMixin):
    """Model representing an earthquake event."""
    
    __tablename__ = "earthquakes"  # Table name for the model
    
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    magnitude = db.Column(db.Float, nullable=False)  # Float for magnitude
    location = db.Column(db.String, nullable=False)  # String for location
    year = db.Column(db.Integer, nullable=False)  # Integer for year

    def __repr__(self):
        return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"
