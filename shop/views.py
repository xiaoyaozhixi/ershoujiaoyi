import math
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *
from shop.models import CltGoods
from order.models import CartInfo
# Create your views here


def loginValid(func):
    def inner(request, *args, **kwargs):
        username = request.session.get('username')
        if username is not None:
            return func(request, *args, **kwargs)
        else:
            url = request.META.get('HTTP_REFERER')
            response = HttpResponseRedirect('/login/')
            response.set_cookie('url', url)
            return response
    return inner


def main(request):
    book_list = ShopInfo.objects.filter(type='book', status=1)[:3]
    digital_list = ShopInfo.objects.filter(type='digital', status=1)[:3]
    cloth_list = ShopInfo.objects.filter(type='cloth', status=1)[:3]
    daily_list = ShopInfo.objects.filter(type='daily', status=1)[:3]
    game_list = ShopInfo.objects.filter(type='game', status=1)[:3]
    other_list = ShopInfo.objects.filter(type='other', status=1)[:3]
    context = {'book_list': book_list, 'digital_list': digital_list, 'cloth_list': cloth_list, 'daily_list': daily_list,
               'game_list': game_list, 'other_list': other_list}
    return render(request, 'shop/main.html', context)


def book_list(request):
    page = int(request.GET.get('page', 1))
    page_size = 10  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * page_size
    book_list = ShopInfo.objects.filter(type='book', status=1)[start:end]
    total_count = ShopInfo.objects.filter(type='book', status=1).count()
    page_str_list = []
    plus = 5  # 当前页面 前后几页的数值
    total_page = math.ceil(total_count / 4)
    if total_page < 2 * plus + 1:  # 页面过少，起始和结束页码改为1和总页面数
        start_page = 1
        end_page = total_page
    elif page < 1 + plus:
        start_page = 1
        end_page = page + plus
    elif page + plus > total_page:
        start_page = page - plus
        end_page = total_page
    else:
        start_page = page - plus  # 当前页面
        end_page = page + plus
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page <= 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:  # 如果是当前所在页面，添加激活样式
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        page_str_list.append(ele)
    # 下一页
    if page < total_page:  # 判断是否超过总页数
        next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        next = '<li><a href="?page={}">下一页</a></li>'.format(total_page)
    page_str_list.append(next)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page))
    # 分页搜索框
    search_string = '''
                <form method="get">
                <div class="input-group" style="width:200px">
                <input type="text" name="page" class="form-control" value="" placeholder="页码">
                <span class="input-group-btn">
                <button class="btn btn-default" type="submit">跳转</button></span>
                </div>
                </form>
                '''
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {'book_list': book_list, 'page_string': page_string}
    return render(request, 'shop/book_list.html', context)


def digital_list(request):
    page = int(request.GET.get('page', 1))
    page_size = 10  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * page_size
    digital_list = ShopInfo.objects.filter(type='digital', status=1)[start:end]
    total_count = ShopInfo.objects.filter(type='digital', status=1).count()
    page_str_list = []
    plus = 5  # 当前页面 前后几页的数值
    total_page = math.ceil(total_count / 4)
    if total_page < 2 * plus + 1:  # 页面过少，起始和结束页码改为1和总页面数
        start_page = 1
        end_page = total_page
    elif page < 1 + plus:
        start_page = 1
        end_page = page + plus
    elif page + plus > total_page:
        start_page = page - plus
        end_page = total_page
    else:
        start_page = page - plus  # 当前页面
        end_page = page + plus
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page <= 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:  # 如果是当前所在页面，添加激活样式
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        page_str_list.append(ele)  # 添加到一个列表中
    # 下一页
    if page < total_page:  # 判断是否超过总页数
        next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        next = '<li><a href="?page={}">下一页</a></li>'.format(total_page)
    page_str_list.append(next)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page))
    # 分页搜索框
    search_string = '''
                    <form method="get">
                    <div class="input-group" style="width:200px">
                    <input type="text" name="page" class="form-control" value="" placeholder="页码">
                    <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">跳转</button></span>
                    </div>
                    </form>
                    '''
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {'digital_list': digital_list, 'page_string': page_string}
    return render(request, 'shop/digital_list.html', context)


def cloth_list(request):
    page = int(request.GET.get('page', 1))
    page_size = 10  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * page_size
    cloth_list = ShopInfo.objects.filter(type='cloth', status=1)[start:end]
    total_count = ShopInfo.objects.filter(type='cloth', status=1).count()
    page_str_list = []
    plus = 5  # 当前页面 前后几页的数值
    total_page = math.ceil(total_count / 4)
    if total_page < 2 * plus + 1:  # 页面过少，起始和结束页码改为1和总页面数
        start_page = 1
        end_page = total_page
    elif page < 1 + plus:
        start_page = 1
        end_page = page + plus
    elif page + plus > total_page:
        start_page = page - plus
        end_page = total_page
    else:
        start_page = page - plus  # 当前页面
        end_page = page + plus
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page <= 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:  # 如果是当前所在页面，添加激活样式
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        page_str_list.append(ele)
    # 下一页
    if page < total_page:  # 判断是否超过总页数
        next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        next = '<li><a href="?page={}">下一页</a></li>'.format(total_page)
    page_str_list.append(next)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page))
    # 分页搜索框
    search_string = '''
                    <form method="get">
                    <div class="input-group" style="width:200px">
                    <input type="text" name="page" class="form-control" value="" placeholder="页码">
                    <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">跳转</button></span>
                    </div>
                    </form>
                    '''
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {'cloth_list': cloth_list, 'page_string': page_string}
    return render(request, 'shop/cloth_list.html', context)


def game_list(request):
    page = int(request.GET.get('page', 1))
    page_size = 10  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * page_size
    game_list = ShopInfo.objects.filter(type='game', status=1)[start:end]
    total_count = ShopInfo.objects.filter(type='game', status=1).count()
    page_str_list = []
    plus = 5  # 当前页面 前后几页的数值
    total_page = math.ceil(total_count / 4)
    if total_page < 2 * plus + 1:  # 页面过少，起始和结束页码改为1和总页面数
        start_page = 1
        end_page = total_page
    elif page < 1 + plus:
        start_page = 1
        end_page = page + plus
    elif page + plus > total_page:
        start_page = page - plus
        end_page = total_page
    else:
        start_page = page - plus  # 当前页面
        end_page = page + plus
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page <= 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:  # 如果是当前所在页面，添加激活样式
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        page_str_list.append(ele)
    # 下一页
    if page < total_page:  # 判断是否超过总页数
        next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        next = '<li><a href="?page={}">下一页</a></li>'.format(total_page)
    page_str_list.append(next)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page))
    # 分页搜索框
    search_string = '''
                    <form method="get">
                    <div class="input-group" style="width:200px">
                    <input type="text" name="page" class="form-control" value="" placeholder="页码">
                    <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">跳转</button></span>
                    </div>
                    </form>
                    '''
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {'game_list': game_list, 'page_string': page_string}
    return render(request, 'shop/game_list.html', context)


def daily_list(request):
    page = int(request.GET.get('page', 1))
    page_size = 10  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * page_size
    daily_list = ShopInfo.objects.filter(type='daily', status=1)[start:end]
    total_count = ShopInfo.objects.filter(type='daily', status=1).count()
    page_str_list = []
    plus = 5  # 当前页面 前后几页的数值
    total_page = math.ceil(total_count / 4)
    if total_page < 2 * plus + 1:  # 页面过少，起始和结束页码改为1和总页面数
        start_page = 1
        end_page = total_page
    elif page < 1 + plus:
        start_page = 1
        end_page = page + plus
    elif page + plus > total_page:
        start_page = page - plus
        end_page = total_page
    else:
        start_page = page - plus  # 当前页面
        end_page = page + plus
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page <= 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:  # 如果是当前所在页面，添加激活样式
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        page_str_list.append(ele)
    # 下一页
    if page < total_page:  # 判断是否超过总页数
        next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        next = '<li><a href="?page={}">下一页</a></li>'.format(total_page)
    page_str_list.append(next)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page))
    # 分页搜索框
    search_string = '''
                    <form method="get">
                    <div class="input-group" style="width:200px">
                    <input type="text" name="page" class="form-control" value="" placeholder="页码">
                    <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">跳转</button></span>
                    </div>
                    </form>
                    '''
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {'daily_list': daily_list, 'page_string': page_string}
    return render(request, 'shop/daily_list.html', context)


def other_list(request):
    page = int(request.GET.get('page', 1))
    page_size = 10  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * page_size
    other_list = ShopInfo.objects.filter(type='other', status=1)[start:end]
    total_count = ShopInfo.objects.filter(type='other', status=1).count()
    page_str_list = []
    plus = 5  # 当前页面 前后几页的数值
    total_page = math.ceil(total_count / 4)
    if total_page < 2 * plus + 1:  # 页面过少，起始和结束页码改为1和总页面数
        start_page = 1
        end_page = total_page
    elif page < 1 + plus:
        start_page = 1
        end_page = page + plus
    elif page + plus > total_page:
        start_page = page - plus
        end_page = total_page
    else:
        start_page = page - plus  # 当前页面
        end_page = page + plus
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page <= 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    page_str_list.append(prev)
    for i in range(start_page, end_page + 1):
        if i == page:  # 如果是当前所在页面，添加激活样式
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)  # 生成多行页码li
        page_str_list.append(ele)
    # 下一页
    if page < total_page:  # 判断是否超过总页数
        next = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        next = '<li><a href="?page={}">下一页</a></li>'.format(total_page)
    page_str_list.append(next)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page))
    # 分页搜索框
    search_string = '''
                    <form method="get">
                    <div class="input-group" style="width:200px">
                    <input type="text" name="page" class="form-control" value="" placeholder="页码">
                    <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">跳转</button></span>
                    </div>
                    </form>
                    '''
    page_str_list.append(search_string)
    page_string = mark_safe("".join(page_str_list))
    context = {'other_list': other_list, 'page_string': page_string}
    return render(request, 'shop/other_list.html', context)


@loginValid
def release_goods(request):
    context = {}
    return render(request, 'shop/release_goods.html', context)


@loginValid
def release(request):
    username = request.session.get('username')
    post = request.POST
    goods = ShopInfo()
    goods.title = post.get('title')
    goods.type = post.get('type')
    goods.price = post.get('price')
    goods.num = post.get('number')
    goods.picture = request.FILES.get('picture')
    goods.description = post.get('description')
    goods.owner = UserInfo.objects.get(username=username)
    goods.save()
    return redirect(reverse('shop:main'))


def clt_goods(request, pk):
    try:
        user = request.session.get('username')
        goods = ShopInfo.objects.get(id=pk)
        new_clt_goods = CltGoods()
        new_clt_goods.who_clt = user
        new_clt_goods.clt_relation_note = goods
        new_clt_goods.owner = goods.owner.username
        new_clt_goods.title = goods.title
        new_clt_goods.save()
        return redirect(reverse('user:collection'))
    except Exception as err:
        print('收藏失败', err)


@loginValid
def details(request, pk):
    goods = ShopInfo.objects.get(id=pk)
    user = UserInfo.objects.filter(id=goods.owner.id)
    context = {'goods': goods, 'user': user}
    return render(request, 'shop/goods_details.html', context)


@loginValid
def rewrite_goods(request, pk):
    goods = ShopInfo.objects.get(id=pk)
    if request.method == "GET":
        context = {'goods': goods}
        return render(request, 'shop/rewrite_goods.html', context)
    else:
        post = request.POST
        picture = request.FILES.get('picture')
        description = post.get('description')
        if picture:
            goods.picture = picture
        goods.title = post.get('title')
        goods.type = post.get('type')
        goods.price = post.get('price')
        goods.num = post.get('number')
        if int(post.get('number')) > 0:
            goods.status = 1
        goods.description = description
        goods.save()
        return redirect(reverse('shop:main'))


def delete_goods(request, pk):
    goods = ShopInfo.objects.filter(id=pk)
    goods.delete()
    return redirect(reverse('shop:main'))


def add_to_cart(request, pk):
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    goods = ShopInfo.objects.get(id=pk)
    price = goods.price
    cart = CartInfo(buyer=user, goods=goods, price=price)
    cart.save()
    return redirect(reverse('user:cart'))


@loginValid
def search_result(request):
    search_title = request.GET['search_title']
    search_goods = ShopInfo.objects.filter(title__contains=search_title)
    count = ShopInfo.objects.filter(title__contains=search_title).count()
    context = {'search_goods': search_goods, 'search_title': search_title, 'count': count}
    return render(request, 'shop/search_result.html', context)
