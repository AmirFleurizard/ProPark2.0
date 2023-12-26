from models import Building
from app import db
#test
Bio = Building(35.31266195, -80.742022, 'Bioinformatics')
db.session.add(Bio)
db.session.commit()
