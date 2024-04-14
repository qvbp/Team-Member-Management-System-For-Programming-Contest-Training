"""
自定义的分页组件，以后如果想要使用这个分页的组件，你需要做如下几件事：

在视图函数中：
    def num_list(request):

        # 1.根据自己的情况去筛选自己的数据
        query_set = models.PrettyNum.objects.all()

        # 2.实例化分页对象
        page_object = Pageination(request, query_set)

        context = {
            'search_data': search_data,

            'query_set': page_object.page_query_set,   # 分完页的数据
            "page_string": page_object.html()    # 页码
        }

        # # 获取所有的靓号列表
        # query_set = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

        return render(request, 'num_list.html', context)

在HTML页面中
    {% for obj in query_set %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""
from django.utils.safestring import mark_safe
import copy


class Pageination(object):
    def __init__(self, request, query_set, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param query_set: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/num/list/?page=12
        :param plus: 显示当前页的 前或后几页（页码）
        """
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        # 1.根据用户想要访问的页码计算出起止位置
        page = request.GET.get(page_param, "1")  # 获得传到url中的page，如果没有穿的话默认第1页
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start_index = (page - 1) * page_size
        self.end_index = page * page_size

        self.page_query_set = query_set[self.start_index:self.end_index]
        self.page_param = page_param

        # 数据总条数
        total_count = query_set.count()

        # 计算出总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1

        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出，显示当前页的前5页和后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，都没有达到11页
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中的数据比较多 > 11页

            # 当前页<5时(小的极值)
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus
            else:
                # 当前页>5
                # 当前页+5 > 总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])

        # 首页
        page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        """
            <li><a href="#">1</a></li>
            <li><a href="#">2</a></li>
            <li><a href="#">3</a></li>
            <li><a href="#">4</a></li>
            <li><a href="#">5</a></li>
        """
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
            <li>
                <form style="float: left; margin-left: -1px"  method="get">
                    <input name="page"
                           style="position: relative; float: left; display: inline-block; width: 80px; border-radius:0;"
                           type="text"  class="form-control" placeholder="页码" required="required">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
            """

        page_str_list.append(search_string)
        page_string = mark_safe(''.join(page_str_list))

        return page_string


