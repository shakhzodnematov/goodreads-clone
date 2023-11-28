from django.http import JsonResponse
from django.views import View

from books.models import BookReview


class BookReviewDetailAPIView(View):
    def get(self, request, id):
        book_review = BookReview.objects.get(id=id)

        json_response = {
            "id": book_review.id,
            "stars_given": book_review.stars_given,
            "comment": book_review.comment
        }

        return JsonResponse(json_response)
