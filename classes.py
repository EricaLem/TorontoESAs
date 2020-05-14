
class Review:

    counter = 1

    # FUNCTIONS
    # Function 1. Initialize
    def __init__( self, date, condition, animals, comment):

        # Keep track of ID number
        self.id = Review.counter
        Review.counter +=1

        # Keep track of reviewers
        self.reviewers = []

        # Initialize Review object
        self.date = date
        # self.user_id = User.id
        self.condition = condition
        self.animals = animals
        self.comment = comment

    # Function 2. Print details
    # So the Review class knows how to print info about itself
    def print_info(self):
        print(f"Date of review: {self.date}")
        print(f"ESA ID: {self.id}")
        print(f"ESA condition: {self.condition}")
        print(f"Animal/s sighted? {self.animals}")
        print(f"Details: {self.comment}")
        # print(f"Reviewer: {self.user_id}")
        print()
        print("Reviewers:")
        for reviewer in self.reviewers:
            print(f"{reviewer.username}")

    # Function 3. Add review (u = user object; self = review object)
    def add_review(self, u):
        self.reviewers.append(u)
        u.review_id = self.id

class User:

    counter = 1
    # FUNCTIONS
    # Function 1. Initialize
    def __init__( self, username, password):

        # Keep track of ID number
        self.id = User.counter
        User.counter +=1

        # Initialize User object
        self.id = id
        self.username = username
        self.password = password

def main():

    # Create Review (calls __init__)
    r1 = Review(date="June 15, 2020", condition="Pristine", animals=True, comment="Yellow-bellied woodpecker")

    # Create Users
    erica = User(username="ericalem", password="mltmjm")
    julien = User(username="jem", password="mltmel")

    # Add Users to Review
    r1.add_review(erica)
    r1.add_review(julien)

    r1.print_info()

if __name__ == "__main__":
    main()