from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 2
    # page_query_param = "pagenum"
    invalid_page_message = "Invalid Page Number"
    page_size_query_param = "size"
    max_page_size = 3