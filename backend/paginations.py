from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return url.replace(f'?page={self.page.number}', f'?page={page_number}', 1)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        return url.replace(f'?page={self.page.number}', f'?page={page_number}', 1)

    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class GoodPagination(CustomPagination):
    page_size = 15


class OrderPagination(CustomPagination):
    page_size = 10


class UserPagination(CustomPagination):
    page_size = 16
