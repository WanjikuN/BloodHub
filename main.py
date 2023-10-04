from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table,DateTime,CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from datetime import datetime
 
engine = create_engine('sqlite:///bloodhub.db')

Base = declarative_base()
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
# Donation - Donor -> one-to-many
# Donation - Hospital -> one-to-many
# Donation - BloodReceiver  -> one-to-many
# BloodReceiver - Hospital  -> one-to-many
# Donor - Hospital -> many-to-many

#Classes
class Donor(Base):
    __tablename__ = 'donors'
    __table_args__ =(
        CheckConstraint(
        "blood_type IN ('A', 'B', 'AB', 'O')",
        name="blood_types"
    )
    )
    
    id = Column(Integer(), primary_key=True)
    donor_name = Column(String())
    blood_type = Column(String())

class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer(), primary_key=True)
    amount = Column(Integer())
    donation_date = Column(DateTime, default=datetime.now())

    
class Hospital(Base):
    __tablename = 'hospitals'

    id = Column(Integer(), primary_key = True)
    hospital_name = Column(String())


class BloodReceiver(Base):
    __tablename__ = 'recepints'
    __table_args__ =(
        CheckConstraint(
        "blood_type IN ('A', 'B', 'AB', 'O')",
        name="blood_types"
    )
    )
    id = column(Integer(), primary_key =True)
    recepient_name = Column(String())
    blood_type = Column(String())