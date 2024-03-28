import math
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from hashlib import sha1
from django.utils.safestring import mark_safe
from order.models import *
from shop.models import CltGoods
from .models import *
from user.form import *
from django.urls import reverse
# Create your views here.


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


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'uname': uname}
    return render(request, 'user/login.html', context)


def login_handle(request):
    post = request.POST
    name = post.get('name')
    password = post.get('password')
    user = UserInfo.objects.filter(username=name)
    #print(name)
    if len(user) == 1:
        s1 = sha1()
        s1.update(password.encode('utf8'))
        if s1.hexdigest() == user[0].password:
            request.session['user_id'] = user[0].id
            request.session['username'] = user[0].username
            return redirect(reverse('shop:main'))
        else:
            context = {'title': '用户登录', 'name': name, 'password': password, 'error_msg': '密码错误'}
            return render(request, 'user/login.html', context)
    else:
        context = {'title': '用户登录',  'name': name, 'password': password, 'error_msg': '用户名错误'}

        return render(request, 'user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')


def register(request):
    context = {}
    return render(request, 'user/register.html', context)


def register_handle(request):
    post = request.POST
    username = post.get('username')
    password = post.get('password')
    password2 = post.get('password2')
    if password != password2:
        return redirect('/register/')
    else:
        s1 = sha1()
        s1.update(password.encode('utf8'))
        user = UserInfo()
        user.username = username
        user.password = s1.hexdigest()
        user.save()
        print('注册成功')
        return redirect('/')


def reset_password(request):
    context = {}
    return render(request, 'user/reset_password.html', context)


def reset_password_handle(request):
    post = request.POST
    username = post.get('username')
    password = post.get('password')
    password2 = post.get('password2')
    user = UserInfo.objects.get(username=username)
    if not user:
        return render(request, 'user/reset_password.html', {'error_msg': '账号不存在'})
    elif password != password2:
        return render(request, 'user/reset_password.html', {'error_msg': '两次密码不一致'})
    s1 = sha1()
    s1.update(password.encode('utf8'))
    user.password = s1.hexdigest()
    user.save()
    print('重置成功')
    return redirect('/')


@loginValid
def user_center(request):
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    context = {'user': user}
    return render(request, 'user/user_center.html', context)


@loginValid
def user_change(request):
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    context = {'user': user}
    return render(request, 'user/user_change.html', context)


@loginValid
def user_change_handle(request):
    post = request.POST
    username = request.session.get('username')
    picture = request.FILES.get('picture')
    sex = post.get('sex')
    phone = post.get('phone')
    address = post.get('address')
    user = UserInfo.objects.get(username=username)
    if picture:
        user.picture = picture
    user.sex = sex
    user.phone = phone
    user.address = address
    user.save()
    return redirect('/user_center/')


@loginValid
def change_password(request):
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    if request.method == "GET":
        form = Change_password()
        return render(request, 'user/change_password.html', {'form': form})
    else:
        form = Change_password(request.POST)
        if form.is_valid():
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            password3 = request.POST.get("password3")
            s1 = sha1()
            s1.update(password1.encode('utf8'))
            s2 = sha1()
            s2.update(password2.encode('utf8'))
            if s1.hexdigest() != user.password:
                print('密码错误！')
                return render(request, 'user/change_password.html', {'form': form})
            elif password2 != password3:
                print('确认密码不一致！')
                return render(request, 'user/change_password.html', {'form': form})
            user.password = s2.hexdigest()
            user.save()
            return redirect('/user_center/')


@loginValid
def collection(request):
    user = request.session.get('username')
    page = int(request.GET.get('page', 1))
    page_size = 6  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * page_size
    collects = CltGoods.objects.filter(who_clt=user).order_by('-clt_time')[start:end]
    total_count = CltGoods.objects.filter(who_clt=user).count()
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
    return render(request, 'user/collection.html', {'collects': collects, 'page_string': page_string})


def remove_clt_goods(request, pk):
    try:
        user = request.session.get('username')
        CltGoods.objects.filter(who_clt=user, id=pk).delete()
        return redirect('/collection/')
    except Exception as err:
        print('取消失败', err)
        return redirect('/collection/')


@loginValid
def my_order(request):
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    page = int(request.GET.get('page', 1))
    page_size = 3  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * page_size
    user_order = OrderInfo.objects.filter(buyer=user)[start:end]
    total_count = OrderInfo.objects.filter(buyer=user).count()
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
    context = {'user_order': user_order, 'page_string': page_string}
    return render(request, 'user/my_order.html', context)


@loginValid
def my_post(request):
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    page = int(request.GET.get('page', 1))
    page_size = 3  # 每一页记录个数
    start = (page - 1) * page_size
    end = page * 3
    user_post = ShopInfo.objects.filter(owner=user)[start:end]
    total_count = ShopInfo.objects.filter(owner=user).count()
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
    context = {'user_post': user_post, "page_string": page_string}
    return render(request, 'user/my_post.html', context)


@loginValid
def my_cart(request):
    return redirect((reverse('user:cart')))


@loginValid
def cart(request):
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    carts = CartInfo.objects.filter(buyer=user)
    cart_list = []
    total_price = 0
    for one in carts:
        cart_list.append(one)
        total_price += one.price * one.number
    total = len(cart_list)
    return render(request, 'user/cart.html', locals())


def delete_cart(request):
    goods_id = request.GET['id']
    username = request.session.get('username')
    user = UserInfo.objects.get(username=username)
    cart2 = CartInfo.objects.filter(buyer=user, goods_id=goods_id)
    cart2.delete()
    return redirect((reverse('user:cart')))
