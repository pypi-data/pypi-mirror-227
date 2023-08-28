from examon_core.examon_item import examon_item


@examon_item(choices=[
    'Incorrect Answer 1', 'Incorrect Answer 2'],
    tags=['tag1', 'tag2'])
def question():
    return 'Hello'
