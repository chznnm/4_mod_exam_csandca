from faker import Faker
faker = Faker()
class DataGenerator:

    @staticmethod
    def generate_random_password():
        return faker.password()

    @staticmethod
    def generate_random_email():
        return faker.email()

    @staticmethod
    def generate_random_name():
        return faker.name()