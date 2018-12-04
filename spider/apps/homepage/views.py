from django.shortcuts import render,redirect
from . import check_user
from . import  douyin_info
from . import  douyin_video

def spider(request):
    url = request.GET.get('search')
    try:
        item = douyin_info.spider(url)
        start = douyin_video.Doyin_Download(url)
        video_url = start.get_download_url(start.get_url())
    except Exception as e:
        print(e)
    if 'item' in locals() and 'video_url' in locals():
        return render(request, 'homepage/search.html', {'item': item, 'video_url': video_url,'uname':request.session['user_name']})
    message='输入链接无效'
    return  render(request,'homepage/index.html',{'uname':request.session['user_name'],'message':message})


def index(request):
    #根据身份认证是否通过执行不同的响应
    if check_user.check_user(request):
        return render(request,'homepage/index.html',{'uname':request.session['user_name']})
    return redirect('/')

def search(request):
    # 根据身份认证是否通过执行不同的响应
    if check_user.check_user(request):
        return spider(request)
    return redirect('/')

