from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    news = News.objects.all().order_by('-date_published')
    return render(request, 'news/list.html', {'news_list': news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'news/detail.html', {'news': news_item})