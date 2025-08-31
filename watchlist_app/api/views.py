# pyright: reportIncompatibleMethodOverride=false, reportAttributeAccessIssue=false

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView

from watchlist_app.api import pagination, permissions, serializers, throttling
from watchlist_app.models import Review, StreamPlatform, WatchList


class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self) -> QuerySet[Review]:
        # DRF provides request.query_params; Pylance sometimes can't infer it.
        username = self.request.query_params.get("username", None)
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]

    def get_queryset(self) -> QuerySet[Review]:
        return Review.objects.all()

    def perform_create(self, serializer) -> None:
        pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user
        )

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data["rating"]
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data["rating"]
            ) / 2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    """
    GET /api/watch/<pk>/reviews/

    Supports:
      - pagination (global DRF setting)
      - filtering: ?rating=5&review_user__username=maro
      - search:    ?search=banger
      - ordering:  ?ordering=-created   or ?ordering=rating
    """
    serializer_class = serializers.ReviewSerializer
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]

    # ✅ enable filters + search + ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["rating", "review_user__username"]   # add "active" if your Review has it
    search_fields = ["description"]
    ordering_fields = ["created", "rating", "id"]            # use "created_at" if that's your field

    def get_queryset(self) -> QuerySet[Review]:
        pk = self.kwargs["pk"]
        # if FK is named 'watchlist', this works; DRF also accepts watchlist_id=pk
        return Review.objects.filter(watchlist_id=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = "review-detail"


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]


class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
