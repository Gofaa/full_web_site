from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from hitcount.utils import get_hitcount_model

from project_site.custom_permissions import OnlyLoggedSuperUser

#from django.views.generic import  TemplateView
from .models import News,  Category
from .forms import ContactForm, CommentForm

"""
#class HomePageView(TemplateView):
#    template_name = 'news/index.html'

class news_list(ListView):
    model = News
    template_name = 'news/news_list.html'
    #context_object_name = "news_list"


class news_detail(DetailView):
    model = News
    template_name = 'news/news_detail.html'

#class IndexView(request):
#    news = News.objects.filter(status = News.Status.Published)
#    categories

"""
def news_list(request):
    news_list = News.objects.filter(status=News.Status.Published) # Published bo'lganlarni publish qiladi
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context)
from hitcount.views import HitCountDetailView, HitCountMixin


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    #hitcount logic Ko'rishlar soni
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = news.comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi comment obyekti yaratiladi lekin MB ga saqlanmaydi
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # Comment egasini so'rov yuborgan userga bog'ladik
            new_comment.user = request.user
            # MB ga saqlash
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        "news": news,
        'new_comment': new_comment,
        'comments': comments,
        'comment_form': comment_form,
        'comment_count': comment_count,

    }
    return render(request, "news/news_detail.html", context)


# def IndexView(request):
#     categories = Category.objects.all()
#     news_list = News.objects.all().order_by('-publish_time')[:6]
#     first_local_news = News.objects.all().filter(category__name='Maxalliy').order_by("-publish_time")[:1]
#     local_news = News.objects.all().filter(category__name='Maxalliy').order_by("-publish_time")[1:6]
#     context = {
#         'news_list': news_list,
#         'categories': categories,
#         'local_news': local_news,
#         'first_local_news': first_local_news,
#     }
#
#     return render(request, "news/index.html", context)

class IndexView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.objects.all().order_by('-publish_time')[:6]
        context['local_news'] = News.objects.all().filter(category__name='Maxalliy').order_by("-publish_time")[:5]
        context['foreign_news'] = News.objects.all().filter(category__name='Xorij').order_by("-publish_time")[:5]
        context['technology_news'] = News.objects.all().filter(category__name='Texnalogiya').order_by("-publish_time")[:5]
        context['sport_news'] = News.objects.all().filter(category__name='Sport').order_by("-publish_time")[:5]
        return context

# def ContactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse(" Biz bilan bog'langaningiz uchun raxmat")
#     context = {
#         "form": form
#     }

#    return render(request, 'news/contact.html', context)

class ContactPageView(TemplateView):
    template_name = "news/contact.html"

    def get(self,request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self,request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaningiz uchun tashakkur </h2>")
        context = {
            "form": form
        }

        return render(request, 'news/contact.html', context)




def NoteFoundPage(request):
    context = {

    }

    return  render(request, 'news/404.html', context)


class LocalNewsView(ListView):
    model = News
    template_name = "news/mahalliy.html"
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.objects.filter(status=News.Status.Published,  category__name="Maxalliy")
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = "news/xorij.html"
    context_object_name = 'xorijiy_yangiliklar'
    def get_queryset(self):
        news = self.model.objects.filter(status=News.Status.Published,  category__name="Xorij")
        return news

class SportNewsView(ListView):
    model = News
    template_name = "news/sport.html"
    context_object_name = 'sport_yangiliklar'
    def get_queryset(self):
        news = self.model.objects.filter(status=News.Status.Published,  category__name="Sport")
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = "news/texnalogiya.html"
    context_object_name = 'texnalogiya_yangiliklar'
    def get_queryset(self):
        news = self.model.objects.filter(status=News.Status.Published,  category__name="Texnalogiya")
        return news



class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = "crud/news_update.html"

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = "crud/news_delete.html"
    success_url = reverse_lazy("index_page")

class NewsCreateView(OnlyLoggedSuperUser ,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title','title_uz', 'title_en', 'title_ru', 'slug', 'body', 'body_uz', 'body_ru', 'body_en', 'image', 'category', 'status')

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_user = User.objects.filter(is_superuser=True)
    context = {
        'admin_user': admin_user
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )






