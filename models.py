from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Table 1. Review
class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column( db.Integer, primary_key=True )
    date = db.Column( db.DateTime, nullable=False )
    condition = db.Column( db.String, nullable=False )
    animals = db.Column( db.Boolean, nullable=False )
    comment = db.Column( db.String, nullable=True )
    user_id = db.Column( db.Integer, db.ForeignKey("users.id"), nullable=False )

# Table 2. User
class User(db.Model):
    __tablename__ = "users"
    id = db.Column( db.Integer, primary_key=True )
    username = db.Column( db.String, nullable=False )
    password = db.Column( db.String, nullable=False )
    postal_code = db.Column( db.String, nullable=False )

# Table 3. ESA
# for ESA_NAME, ESA_NUM, Shape_Area, Shape_Length, geometry
class ESA(db.Model):
    __tablename__ = "esas"
    id = db.Column( db.Integer, primary_key=True )
    ESA_NAME = db.Column( db.String, nullable=False )
    ESA_NUM = db.Column( db.Integer, nullable=False )
    Shape_Area = db.Column( db.Float, nullable=False )
    Shape_Length = db.Column( db.Float, nullable=False )
    geometry = db.Column( db.Text, nullable=False )

#	def add_passenger(self, name):
#		p = Passenger(name=name, flight_id=self.id)
#		db.session.add(p)
#		db.session.commit()
