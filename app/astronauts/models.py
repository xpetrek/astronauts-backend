from app import db

class Astronaut(db.Model):
    __tablename__ = 'astronauts'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column('firstName', db.String(50))
    lastName = db.Column('lastName', db.String(50))
    dateOfBirth = db.Column('dateOfBirth', db.String(10))
    superpower = db.Column('superpower', db.String(50))

    def serialize(self):
        return {'id': self.id,
                'firstName': self.firstName,
                'lastName': self.lastName,
                'dateOfBirth': self.dateOfBirth,
                'superpower': self.superpower,
                }

    def reduced_serialize(self):
       return {'id': self.id,
                'firstName': self.firstName,
                'lastName': self.lastName,
                'dateOfBirth': self.dateOfBirth,
                'superpower': self.superpower,
                }
