def assert_movie_data_matches(expected,received):
    assert expected["name"] == received["name"],f'Expected:{expected['name']}, Received:{received['name']}'
    assert expected["imageUrl"] == received["imageUrl"],f'Expected:{expected['imageUrl']}, Received:{received['imageUrl']}'
    assert expected["price"] == received["price"],f'Expected:{expected['price']}, Received:{received['price']}'
    assert expected["description"] == received["description"],f'Expected:{expected['description']}, Received:{received['description']}'
    assert expected["location"] == received["location"],f'Expected:{expected['location']}, Received:{received['location']}'
    assert expected["published"] == received["published"],f'Expected:{expected['published']}, Received:{received['published']}'

def assert_review_data_matches(expected,received):
    assert expected["rating"] == received["rating"],f'Expected:{expected['rating']}, Received:{received['rating']}'
    assert expected["text"] == received["text"],f'Expected:{expected['text']}, Received:{received['text']}'