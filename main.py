from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table,DateTime,CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship,declarative_base
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

# Association object(Donation - Hospital -> one-to-many)
donor_hospitals = Table(
    'donor_hospitals',
    Base.metadata,
    Column('donor_id', ForeignKey('hospitals.id'),primary_key=True),
    Column('hospital_id', ForeignKey('donors.id'),primary_key=True),
)

#Classes
class Donor(Base):
    __tablename__ = 'donors'
    __table_args__ =(
        CheckConstraint(
        "blood_type IN ('A', 'B', 'AB', 'O')",
        name="blood_types"
        ),
    )
    
    id = Column(Integer(), primary_key=True)
    donor_name = Column(String())
    blood_type = Column(String())

    # relationships
    donation = relationship("Donation", back_populates = ('donor'))
    hospital = relationship("Hospital", secondary = donor_hospitals, back_populates = ('donor'))

class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer(), primary_key=True)
    amount = Column(Integer())
    donation_date = Column(DateTime, default=datetime.now())
    donor_id = Column(Integer(), ForeignKey('donors.id'))
    hospital_id = Column(Integer(), ForeignKey('hospitals.id'))
    bloodreceiver_id = Column(Integer(), ForeignKey('recepients.id'))

     # relationships
    donor = relationship("Donor", back_populates = ('donation'))
    hospital = relationship("Hospital" , back_populates = ('donation'))
    blood_receiver = relationship("BloodReceiver", back_populates = ('donation'))

    
class Hospital(Base):
    __tablename__ = 'hospitals'

    id = Column(Integer(), primary_key = True)
    hospital_name = Column(String())

     # relationships
    donation = relationship("Donation", back_populates = ('hospital'))
    blood_receiver = relationship("BloodReceiver", back_populates = ('hospital'))
    donor = relationship("Donor", secondary = donor_hospitals, back_populates = ('hospital'))



class BloodReceiver(Base):
    __tablename__ = 'recepients'
    __table_args__ =(
        CheckConstraint(
        "blood_type IN ('A', 'B', 'AB', 'O')",
        name="blood_types"
     ),
    )
    id = Column(Integer(), primary_key =True)
    recepient_name = Column(String())
    blood_type = Column(String())
    hospital_id = Column(String(), ForeignKey("hospitals.id"))

    # relationships
    donation = relationship("Donation", ForeignKey("blood_receiver"))
    hospital = relationship("Hospital", back_populates = ('blood_receiver'))
