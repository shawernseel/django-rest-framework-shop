from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class ProductPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'pagenum' #this just changes it to prodcts/?pagenum=2 instead of prodcts/?page=2
    page_size_query_param = 'size' #this enables prodcuts/?size=7
    max_page_size = 6

class ProductLimitOffsetPagination(LimitOffsetPagination):
    pass