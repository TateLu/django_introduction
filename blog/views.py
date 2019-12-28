from django.shortcuts import render

from django.http import HttpResponse

from blog.models import Article

from django.core.paginator import Paginator

# Create your views here.


def hello_world(request):
    return HttpResponse("Hello World")


def article_content(request):
    article = Article.objects.all()[0]
    title = article.title
    brief_content = article.brief_content
    content = article.content
    article_id = article.article_id
    publish_date = article.publish_date
    return_str = 'title: %s, brief_content: %s, ' \
                 'content: %s, article_id: %s, publish_date: %s' % (title,
                                                                    brief_content,
                                                                    content,
                                                                    article_id,
                                                                    publish_date)
    return HttpResponse(return_str)


def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    #获取文章对象list
    all_article = Article.objects.all()
    #按日期倒序排列
    top10_article_list = Article.objects.order_by('-publish_date')[:10]

    #Django自带的Paginator模块，每页6个
    paginator = Paginator(all_article, 6)
    page_num = paginator.num_pages
    print('page num:', page_num)
    #获取属于指定页号的文章list
    page_article_list = paginator.page(page)

    #先把前一页后一页的页号算好
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    #整合模型资源与HTML页面结合
    return render(request, 'blog/index.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top10_article_list': top10_article_list
                  }
                  )


def get_detail_page(request, article_id):
    all_article = Article.objects.all()
    curr_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None

    #枚举文章对象和下标
    for index, article in enumerate(all_article):
        #若是最前一页或最后一页，对应处理
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1
        #找到对应下标对象，以及前一个后一个对象
        if article.article_id == article_id:
            curr_article = article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break

    #按回车符分割文章内容
    section_list = curr_article.content.split('\n')

    #整合模型与对应网页
    return render(request, 'blog/detail.html',
                  {
                      'curr_article': curr_article,
                      'section_list': section_list,
                      'previous_article': previous_article,
                      'next_article': next_article
                  }
                  )
