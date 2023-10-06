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
    # Get all donors
    @classmethod
    def get_donors(cls):
        with Session() as session:
            return session.query(cls).all()

    # Get history of donations made
    def donation_history(self):
        with Session() as session:
            return session.query(Donation).filter_by(donor_id=self.id).all()
            
    # Total donations
    def donation_count(self):
        return len(self.donation_history())
    
    # Eligiblity by age and weight
    def donation_eligibility(self):
        with Session() as session:
            query = session.query(Donor).filter_by(id=self.id).first()
            return f'{True}: {query.donor_name} -> gets to save a life today!'  if 15<= session.query(Donor).filter_by(id=self.id).first().age<=49 and 50<= session.query(Donor).filter_by(id=self.id).first().weight<=80 else f'{False}:(age:15-49, weight:50-80)\n{query.donor_name}-> Age:{query.age} Weight:{query.weight} '
    
    # Donor preferred hospitals
    def preffered_hospitals(self):
        return [hospital.hospital_name for hospital in self.hospital]
            
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
    
    # create a donation
    def create_donation(self, session, amount, donor, hospital, blood_receiver=None):
        donation = Donation(donor=donor, amount=amount, hospital=hospital, blood_receiver=blood_receiver)
        session.add(donation)
        session.commit()
        print("Donated successfully!!")

    # All donations
    @classmethod
    def all_donations(cls):
        with Session() as session:
            return session.query(cls).all()
        
    # number of donations made
    @classmethod
    def count_donations(cls):
        with Session() as session:
            return len(cls.all_donations())

    # total donations
    @classmethod
    def total_donations(cls):
        with Session() as session:
            return sum(donation.amount for donation in session.query(cls).all())

    # total donations to a hospital
    @classmethod
    def total_hospital_donations(cls,hospital):
        with Session() as session:
            return sum(donation.amount for donation in session.query(cls).filter(Donation.hospital_id == hospital.id).all())
        
    # get donations within a date range
    @classmethod
    def donations_within_range(cls, start_date, end_date):
        with Session() as session:
            return session.query(cls).filter(cls.donation_date.between(start_date, end_date)).all()


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
    
    # Get hospital's blood receivers
    def get_blood_receivers(self):
        with Session() as session:
            return session.query(BloodReceiver).filter(BloodReceiver.hospital_id == self.id).all()

    # Hospital's donations
    def get_donations(self):
        with Session() as session:
            return session.query(Donation).filter_by(hospital_id=self.id).all()

    # Hospital's doonors
    def get_donors(self):
        with Session() as session:
            return session.query(Donor).filter(Donor.hospital.any(id=self.id)).all()



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
    
    # all recipients list
    @classmethod
    def all_recipients(cls):
        with Session() as session:
            return session.query(cls).all()

    # recipient's donations
    def get_donations(self, session):
        return session.query(Donation).filter_by(bloodreceiver_id=self.id).all()

    # recipient preferred hospitals
    def preffered_hospitals(self):
        with Session() as session:
            for hospital in self.hospital:
                return hospital.hospital_name
    
if __name__ == "__main__":
    with Session() as session:
        session.query(Donor).delete()
        session.query(Donation).delete()
        session.query(BloodReceiver).delete()
        session.query(Hospital).delete()
        session.commit()
        # create donors
        donor1 = Donor(donor_name="Patricia Wanjiku",  blood_type='A', age= 15, weight=88)
        donor2 = Donor(donor_name="Pat Wan",  blood_type='B', age= 45, weight=108)
        donor3 = Donor(donor_name="Mary Njoki",  blood_type='O', age= 17, weight=58)
        donor4 = Donor(donor_name="Alvin O",  blood_type='AB', age= 55, weight=68)

        session.add_all([donor1, donor2, donor3, donor4])
        session.commit()

        # update donoor details
        donor1.update_donor_details(49)
        donor2.update_donor_details(weight=75)
        session.commit()

        # Print donor eligibility
        print("Donor 1 Eligibility:", donor1.donation_eligibility())
        print("Donor 2 Eligibility:", donor2.donation_eligibility())
        print("Donor 3 Eligibility:", donor3.donation_eligibility())
        print("Donor 4 Eligibility:", donor4.donation_eligibility())

        # Create hospitals
        hospital1 = Hospital(hospital_name="PGH")
        hospital2 = Hospital(hospital_name="St Joseph Hospital")

        session.add_all([hospital1, hospital2])
        session.commit()

        # Add donors to hospitals
        if donor1 not in hospital1.donor:
            hospital1.donor.append(donor1)
        if donor2 not in hospital1.donor:
            hospital1.donor.append(donor2)
        if donor3 not in hospital2.donor:
            hospital2.donor.append(donor3)
        if donor4 not in hospital2.donor:
            hospital2.donor.append(donor4)
        

        session.commit()

        # Create blood receivers
        receiver1 = BloodReceiver(recepient_name="Adam", blood_type='A')
        receiver2 = BloodReceiver(recepient_name="Eve", blood_type='O')

        session.add_all([receiver1, receiver2])
        session.commit()

        # Make donations -Amount is equated to a bag of blood
        donation1 = Donation()
        donation1.create_donation(session,amount=2, donor=donor1, hospital=hospital1, blood_receiver=receiver1)
        
        donation2 = Donation()
        donation2.create_donation(session,amount=1, donor=donor2, hospital=hospital2)
    
        # Print total donations
        print(f"Total Donations: {Donation.total_donations()}")

        # Print donations to a specific hospital
        print(f"Total Donations to {hospital1.hospital_name}: {Donation.total_hospital_donations(hospital1)}")

       