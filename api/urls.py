from django.urls import path

from api.views import BookReviewDetailAPIView

app_name = "api"
urlpatterns = [
    path("reviews/<int:id>/", BookReviewDetailAPIView.as_view(), name="review-detail")
]