from typing import List

from .models import Author


def create_authors_fixture():

    authors: List[Author] = []
    for i in range(1000):
        authors.append(Author(name=f'name_{i}'))

    Author.objects.bulk_create(authors)
