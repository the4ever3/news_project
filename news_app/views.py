from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from .models import News, Category
from .forms import ContactForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from news_project1.custom_permissions import OnlyLoggedSuperUser

def news_list(request):
    news_list = News.objects.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context=context)




def news_detail(request, news):
    news = get_object_or_404(News, slug=news)
    # context = {}
    # hit_count = get_hitcount_model().objects.get_for_object(news)
    comments = news.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #yangi commentni yaratamiz lekn db ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            #db ga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        "news": news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, "news/news_detail.html", context)

def homePageView(request):
    news_list = News.objects.all().order_by('-publish_time')[:5]
    categories = Category.objects.all()
    mahalliy_one = News.objects.all().filter(category__name="MAHALLIY").order_by('-publish_time')[:1]
    mahalliy_news = News.objects.all().filter(category__name="MAHALLIY").order_by('-publish_time')[1:6]
    xorijiy_one = News.objects.all().filter(category__name="XORIJIY").order_by('-publish_time')[:1]
    xorijiy_news = News.objects.all().filter(category__name="XORIJIY").order_by('-publish_time')[1:6]

    context = {
        'news_list': news_list,
        'categories': categories,
        'mahalliy_one': mahalliy_one,
        'mahalliy_news': mahalliy_news,
        'xorijiy_one': xorijiy_one,
        'xorijiy_news': xorijiy_news
    }
    return render(request, 'news/index.html', context)



class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>biz bilan boglanganiz uchun tashakkur</h2>")
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

def page404View(request):
    context = {

    }
    return render(request, 'news/404.html', context)

def singlePageView(request,id):
    news = get_object_or_404(News,id=id)

    context = {
        "news": news
    }
    return render(request, "news/single_page.html", context)


class MahalliyNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_news'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name="MAHALLIY")
        return news


class XorijNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_news'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name="XORIJIY")
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name="SPORT")
        return news


class TexnologiyaNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_news'

    def get_queryset(self):
        news = self.model.objects.all().filter(category__name="TEXNOLOGIYA")
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ("title", "body", "image", "status", "category", )
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ("author", "title", "slug", "body", "image", "status", "category", )


@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsListView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = "barcha_yangiliklar"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

