from .models import Article
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from .forms import ArticleForm
# Create your views here.

@require_http_methods(['GET', 'POST'])  # 2가지 경우에만 함수실행
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)
    


@require_safe  # POST 안들어오니까, db에 변경 요청없을 때 쓰면 됨
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


@require_safe
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


@require_http_methods(['GET', 'POST'])
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)

    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/form.html', context)


@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('articles:index')
