from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.restaurant import Restaurant
from models.customer import Customer
from models.review import Review
from models.base import Base

# Define the database file and create the engine
DATABASE_URI = "sqlite:///restaurant_reviews.db"
engine = create_engine(DATABASE_URI)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create the database tables
Base.metadata.create_all(engine)

# Create sample data
customers = [
    Customer(first_name='John', last_name='Doe'),
    Customer(first_name='Jane', last_name='Smith'),
    Customer(first_name='Valent', last_name='Carols'),
    Customer(first_name='Denis', last_name='Luki')
]

restaurants = [
    Restaurant(name='Pizza Palace', price=2),
    Restaurant(name='Burger Barn', price=3),
    Restaurant(name='Slate', price=1500),
    Restaurant(name='Mawimbi', price=2000)
]

reviews = [
    Review(customer=customers[0], restaurant=restaurants[0], rating=4, comment='Great pizza!'),
    Review(customer=customers[1], restaurant=restaurants[0], rating=5, comment='Best pizza in town!'),
    Review(customer=customers[0], restaurant=restaurants[1], rating=3, comment='Good burgers.'),
    Review(customer=customers[2], restaurant=restaurants[3], rating=3, comment='Best Steak ever!')
]

# Add sample data to the session and commit to the database
session.add_all(customers + restaurants + reviews)
session.commit()

# Test the new methods
print("Customers:")
for customer in session.query(Customer).all():
    print(f"Customer: {customer.first_name} {customer.last_name}")
    favorite = customer.favorite_restaurant(session)  # Pass the session argument
    if favorite:
        print(f"Favorite Restaurant: {favorite.name}")
    else:
        print("No favorite restaurant found.")

    # Test adding a review for the new customer and restaurant
    new_review = customer.add_review(session, restaurants[3], rating=4, comment='Excellent food, drink, and surrounding!')  # Pass the session
    session.commit()
    print(f"Added review: {new_review.comment}")

print("Restaurants:")
for restaurant in session.query(Restaurant).all():
    print(f"{restaurant.name}, Price: {restaurant.price}")
    reviews = [review.full_review() for review in restaurant.reviews]  # Remove () here
    if reviews:
        print(f"Reviews: {reviews}")
    else:
        print("No reviews for this restaurant")

    # Test deleting reviews for the new customer and restaurant
    customers[3].delete_reviews(session, restaurants[3])  # Pass the session
    session.commit()
    print(f"Reviews after deleting for {restaurants[3].name}: {[review.comment for review in customers[3].reviews if review.restaurant == restaurants[3]]}")

# Close the session
session.close()
