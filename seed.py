from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from main import Base, Donor, Donation, Hospital, BloodReceiver
engine = create_engine('sqlite:///bloodhub.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    # Use Faker to generate fake data
    fake = Faker()

    with Session() as session:
        session.query(Donor).delete()
        session.query(Donation).delete()
        session.query(Hospital).delete()
        session.query(BloodReceiver).delete()
        
        session.commit()
        # Create donors
        donors = [
            Donor(
                donor_name=fake.name(),
                blood_type=fake.random_element(elements=('A', 'B', 'AB', 'O')),
                age=fake.random_int(min=15, max=49),
                weight=fake.random_int(min=50, max=80)
            )
            for _ in range(5)  
        ]

        session.add_all(donors)
        session.commit()

        # Update donor details
        donors[0].update_donor_details(49)

        # Print donor eligibility
        print(donors[0].donation_eligibility())

        # Create hospitals
        hospitals = [
            Hospital(hospital_name=fake.company())
            for _ in range(2)  
        ]

        session.add_all(hospitals)
        session.commit()

        # Create blood receivers
        receivers = [
            BloodReceiver(
                recepient_name=fake.name(),
                blood_type=fake.random_element(elements=('A', 'B', 'AB', 'O'))
            )
            for _ in range(2) 
        ]

        session.add_all(receivers)
        session.commit()

        # Make  donations
        donation1 = Donation()
        donation1.create_donation(session,amount=7, donor=donors[0], hospital=hospitals[0], blood_receiver=receivers[0])
        donation2 = Donation()
        donation2.create_donation(session,amount=15, donor=donors[1], hospital=hospitals[1])

        # Print total donations
        print(f"Total Donations: {Donation.total_donations()}")

        # Print donations to a specific hospital
        print(f"Total Donations to {hospitals[0].hospital_name}: {Donation.total_hospital_donations(hospitals[0])}")

       