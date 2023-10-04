from sqlalchemy import create_engine,Column,Integer,String,Table,DateTime,CheckConstraint,ForeignKey
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
    Column('donor_id', ForeignKey('donors.id'),primary_key=True),
    Column('hospital_id', ForeignKey('hospitals.id'),primary_key=True),

)

#Classes
class Donor(Base):
    __tablename__ = 'donors'
    __table_args__ =(
        CheckConstraint(
        "blood_type IN ('A', 'B', 'AB', 'O')",
        name="blood_types"
        ),
        CheckConstraint(
        "age BETWEEN 15 and 49",
        name="age_factor"
        ),
        CheckConstraint(
        "weight BETWEEN 50 and 80",
        name="weight_factor"
        ),
    )
    
    id = Column(Integer(), primary_key=True)
    donor_name = Column(String())
    blood_type = Column(String())
    age = Column(Integer())
    weight = Column(Integer())
    # relationships
    donation = relationship("Donation", back_populates ='donor')
    hospital = relationship("Hospital", secondary = donor_hospitals, back_populates ='donor')

    def __repr__(self):
        return f'\nDONOR:\nName:{self.donor_name}\nBlood Type:{self.blood_type}\nAge:{self.age}\nWeight:{self.weight}\n'
    
    # Update weight and/or age
    def update_donor_details(self, age=age, weight=weight):
        with Session() as session:
            donor_to_update = session.query(Donor).filter_by(id=self.id).first()
            if donor_to_update:
                donor_to_update.age = age
                donor_to_update.weight = weight
                session.commit()


    
class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer(), primary_key=True)
    amount = Column(Integer())
    donation_date = Column(DateTime, default=datetime.now())
    donor_id = Column(Integer(), ForeignKey('donors.id'))
    hospital_id = Column(Integer(), ForeignKey('hospitals.id'))
    bloodreceiver_id = Column(Integer(), ForeignKey('recipients.id'))

     # relationships
    donor = relationship("Donor", back_populates ='donation')
    hospital = relationship("Hospital" , back_populates ='donation')
    blood_receiver = relationship("BloodReceiver", back_populates ='donation')

    def __repr__(self):
        return f'{self.amount}'
    
class Hospital(Base):
    __tablename__ = 'hospitals'

    id = Column(Integer(), primary_key = True)
    hospital_name = Column(String())

     # relationships
    donation = relationship("Donation", back_populates ='hospital')
    blood_receiver = relationship("BloodReceiver", back_populates ='hospital')
    donor = relationship("Donor", secondary = donor_hospitals, back_populates ='hospital')

    def __repr__(self):
        return f'{self.hospital_name}'

class BloodReceiver(Base):
    __tablename__ = 'recipients'
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
    donation = relationship("Donation", back_populates= 'blood_receiver')
    hospital = relationship("Hospital", back_populates ='blood_receiver')

    def __repr__(self):
        return f'\nBLOOD_RECEIVER:\nName:{self.recepient_name}\nBlood Type:{self.blood_type}\n'
    
if __name__ == "__main__":
    with Session() as session:
        donor1 = Donor(donor_name="Patricia Wanjiku",  blood_type='A', age= 15, weight=55)
        session.add(donor1)
        session.commit()
        donor1.update_donor_details(60)
        