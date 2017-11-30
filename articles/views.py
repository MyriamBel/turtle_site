from django.http.response import Http404
from django.shortcuts import render_to_response, redirect, render
from .models import Article, Comments
from django.core.exceptions import ObjectDoesNotExist
from .forms import CommentForm
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage
from datetime import datetime
from django.contrib.auth.models import User

def articles(request, page_number=1):
    try:
        all_articles = Article.objects.all()
        current_page = Paginator(all_articles, 3)
        return render_to_response('articles.html', {'articles': current_page.page(page_number),
                                                    'username': auth.get_user(request).username})
    except EmptyPage:
        raise Http404

@csrf_protect
def article(request, article_id=1):
    try:
        comment_form = CommentForm
        args = {}
        args.update()
        article = Article.objects.get(id=article_id)
        comments = Comments.objects.filter(comments_article_id=article_id)
        args['article'] = article
        args['comments'] = comments
        args['form'] = comment_form
        args['username'] = auth.get_user(request).username
        return render(request, 'article.html', args)
    except ObjectDoesNotExist:
        raise Http404

def addlike(request, article_id, page_number=1):
    page_url = request.POST
    print(page_url)
    if "page" in page_url:
        page_number = page_url.split("/")[-2]
    try:
        if article_id in request.COOKIES:
            redirect('/')
        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            response = redirect(reverse('articlesapp:articles', args=(page_number,)))
            response.set_cookie(article_id, 'test')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect(reverse('articlesapp:articles', args=(page_number, )))

def addcomment(request, article_id):
    if (request.method == 'POST') and ("pause" not in request.session):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_article = Article.objects.get(id=article_id)
            form.save(commit=True)
            request.session.set_expiry(3600)
            request.session['pause'] = True
            return redirect(reverse('articlesapp:article', args=(article_id,)))
    return redirect(reverse('articlesapp:article', args=(article_id,)))
