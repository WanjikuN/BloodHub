from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship 
engine = create_engine('sqlite:///bloodhub.db')

Base = declarative_base()
Session = sessionmaker(bind=engine)

# Donation - Donor -> one-to-many
# Donation - Hospital -> one-to-many
# Donation - BloodReceiver  -> one-to-many
# BloodReceiver - Hospital  -> one-to-many
# Donor - Hospital -> many-to-many

#Classes
class Donor(Base):
    pass
class Donation(Base):
    pass
class Hospital(Base):
    pass
class BloodReceiver(Base):
    pass