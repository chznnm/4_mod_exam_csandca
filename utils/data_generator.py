from faker import Faker
from uuid import uuid4
import datetime
faker = Faker("ru_RU")
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

    @staticmethod
    def generate_random_movie_name():
        return faker.sentence(nb_words=2)

    @staticmethod
    def generate_random_image_url():
        return faker.url()

    @staticmethod
    def generate_random_price():
        return faker.random_int(min=100,max=1500)

    @staticmethod
    def generate_random_location():
        return faker.word(ext_word_list=["MSK","SPB"])

    @staticmethod
    def generate_random_bool():
        return faker.boolean()

    @staticmethod
    def generate_random_genre_id():
        return faker.random_int(min=2,max=10)

    @staticmethod
    def generate_random_description():
        return faker.catch_phrase()

    @staticmethod
    def generate_random_rating():
        return faker.random_int(min=1,max=5)

    @staticmethod
    def generate_random_text_for_review():
        return faker.text()

    @staticmethod
    def generate_random_genre_name():
        return faker.word()

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_random_int(value):
        return faker.random_int(value)