"""
自定义分页组件
在视图函数中：
def xxx_list(request):
    # 1.根据自己的情况区筛选自己的数据
    queryset = Attraction.objects.filter(**data_dict)
    2.实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html()  # 生成页码
    }
    return render(request, 'xxx_list.html', context)
在HTML页面中
    {% for obj in queryset %}
        {{ obj.xxx }}
    {% endfor %}
    <ul class="pagination">
        {{ page_string }}
    </ul>
"""

from django.utils.safestring import mark_safe
import copy
class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如/api/attractionlist/?page=1
        :param plus: 显示当前页的前几页和后几页
        """
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        query_dict.setlist('page', [])

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus
        self.page_param = page_param

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        elif self.page <= self.plus:
            start_page = 1
            end_page = 2 * self.plus + 1
        else:
            start_page = self.page - self.plus
            end_page = self.page + self.plus
        # 页码
        page_str_list = []
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li class="active"><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(prev)
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                li = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                li = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(li)
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li class="active"><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(next)
        search_string = """
            <li>
                <form method="get">
                    <input name="page" type="text" placeholder="页码">
                    <button type="submit">跳转到相应页面</button>
                </form>
            <li>
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
