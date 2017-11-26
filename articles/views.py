from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect, render
from .models import Article, Comments
from django.core.exceptions import ObjectDoesNotExist
from .forms import CommentForm
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.contrib import auth

def basic_one(request):
    view = "basic one"
    html = "<html><body> There is %s </body></html>" % view
    return HttpResponse(html)

def template_two(request):
    view = "template_two"
    t = get_template('base.html')
    html = t.render({'name': view})
    return HttpResponse(html)

def template_three(request):
    view = 'template three'
    return render_to_response(template_name='base.html', context={'name': view})

def articles(request):
    return render_to_response('articles.html', {'articles': Article.objects.all(), 'username': auth.get_user(request).username})

@csrf_protect
def article(request, article_id=1):
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

def addlike(request, article_id):
    try:
        if article_id in request.COOKIES:
            redirect('/')
        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            response = redirect('/')
            response.set_cookie(article_id, 'test')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')

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
