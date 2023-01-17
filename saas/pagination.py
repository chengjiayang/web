from rest_framework.pagination import PageNumberPagination as _PageNumberPagination

# 继承rest_framework的PageNumberPagination类，并将类名写为一样的
class PageNumberPagination(_PageNumberPagination):
    # 指定默认每一页显示的数据条数
    page_size = 10
    # 前端用于指定页号的查询字符串参数名称
    page_query_param = 'page'
    # 指定前端用于指定页号的查询字符串参数的描述
    page_query_description = '获取的页码'
    # 只要设置了page_size_query_param，那么前端就支持指定获取每一页的数据条数，前端传“?s=8”就可以将每一页的数据设置为8条
    page_size_query_param = "size"
    # 前端用于指定每一页的数据条数，查询字符串参数的描述
    page_size_query_description = '每一页数据条数'
    # 设置每一页最大的数据条数
    max_page_size = 500

	# 重写父类的方法给返回的数据增加页号字段
    def get_paginated_response(self, data):
        # 调用父类的实现
        response = super().get_paginated_response(data)
        # 增加页号字段
        response.data['current_num'] = self.page.number
        # 返回新增后的字典
        return response
