import re

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.ratings = {}  
        self.comments = {}

    def rate_product(self, product_id, rating, comment=None):
        self.ratings[product_id] = rating
        if comment:
            self.comments[product_id] = comment

    def get_ratings(self):
        return self.ratings

    def get_comments(self):
        return self.comments


class Product:
    def __init__(self, product_id, name):
        self.product_id = product_id
        self.name = name
        self.total_rating = 0
        self.rating_count = 0

    def add_rating(self, rating):
        self.total_rating += rating
        self.rating_count += 1

    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return self.total_rating / self.rating_count


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def create_account(users):
    username = input("Enter your username: ")
    
    
    while any(user.username == username for user in users):
        print("Username already exists. Please choose a different username.")
        username = input("Enter your username: ")

    email = input("Enter your email: ")
    while not is_valid_email(email):
        print("Invalid email format. Please try again.")
        email = input("Enter your email: ")
    
    user = User(username, email)
    users.append(user)
    print(f"Account created for {username}!")


def rate_products(users, products):
    username = input("Enter your username to rate products: ")
    user = next((u for u in users if u.username == username), None)
    
    if not user:
        print("Username not found. Please create an account or try again.")
        return

    print("\nAvailable Products:")
    for product in products:
        print(f"Product ID: {product.product_id}, Name: {product.name}")

    while True:
        product_id = input("\nEnter the Product ID to rate (or type 'exit' to finish): ")
        if product_id.lower() == 'exit':
            break
        try:
            product_id = int(product_id)
            product = next((p for p in products if p.product_id == product_id), None)
            if product:
                rating = float(input(f"Rate the product '{product.name}' (ID: {product.product_id}) from 1 to 5: "))
                if 1 <= rating <= 5:
                    comment = input("Enter your comment or opinion about this product: ")
                    user.rate_product(product.product_id, rating, comment)
                    product.add_rating(rating)
                    print(f"Thank you for rating '{product.name}' with a score of {rating}!")
                else:
                    print("Rating must be between 1 and 5. Please try again.")
            else:
                print("Invalid Product ID. Please try again.")
        except ValueError:
            print("Please enter a valid number for Product ID or rating.")


def display_ranked_products(products):
    ranked_products = sorted(products, key=lambda p: p.average_rating(), reverse=True)
    print("\nRanked Products by Average Rating:")
    for product in ranked_products:
        print(f"Product ID: {product.product_id}, Name: {product.name}, Average Rating: {product.average_rating():.2f}")


def main():
    products = [
        Product(1, "Laptop"),
        Product(2, "Smartphone"),
        Product(3, "Tablet"),
        Product(4, "Smartwatch"),
    ]

    users = []

    while True:
        print("\n1. Create Account\n2. Rate Products\n3. Display Ranked Products\n4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            create_account(users)
        elif choice == '2':
            if not users:
                print("No users available. Please create an account first.")
                continue
            rate_products(users, products)
        elif choice == '3':
            display_ranked_products(products)
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
