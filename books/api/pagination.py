from rest_framework import pagination

class SmallPagination(pagination.PageNumberPagination):
    page_size = 5