from utils.data_generator import DataGenerator

def generate_edited_movie_data():
    return{
        "name": DataGenerator.generate_random_movie_name(),
        "price": DataGenerator.generate_random_price()
    }

def generate_edited_review_data():
    return {
        "rating": DataGenerator.generate_random_rating(),
        "text": DataGenerator.generate_random_text_for_review()
    }