from django.test import TestCase
from django.urls import reverse

from books.models import Book
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="book1", description="Description1", isbn="111111111")
        book2 = Book.objects.create(title="book2", description="Description2", isbn="222222222")
        book3 = Book.objects.create(title="book3", description="Description3", isbn="333333333")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="book1", description="Description1", isbn="111111111")

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="Description1", isbn="111111111")
        book2 = Book.objects.create(title="Guide", description="Description2", isbn="222222222")
        book3 = Book.objects.create(title="Shoe Dog", description="Description3", isbn="333333333")

        response = self.client.get(reverse("books:list") + "?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=guide")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=shoe")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):
   def test_add_review(self):
       book = Book.objects.create(title="book1", description="Description1", isbn="111111111")
       user = CustomUser.objects.create(
           username="shahzod",
           first_name="Shahzod",
           last_name="Nematov",
           email="shahzod@gmail.com"
       )
       user.set_password("somepass")
       user.save()
       self.client.login(username="shahzod", password="somepass")

       self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
           "stars_given": 3,
           "comment": "Nice book"
       })
       book_reviews = book.bookreview_set.all()

       self.assertEqual(book_reviews.count(), 1)
       self.assertEqual(book_reviews[0].stars_given, 3)
       self.assertEqual(book_reviews[0].comment, "Nice book")
       self.assertEqual(book_reviews[0].book, book)
       self.assertEqual(book_reviews[0].user, user)