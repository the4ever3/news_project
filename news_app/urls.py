from django.urls import path
from .views import news_list, singlePageView, news_detail, homePageView, ContactPageView, page404View, MahalliyNewsView, XorijNewsView, SportNewsView, TexnologiyaNewsView, \
    NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page_view, SearchResultsListView

urlpatterns = [
    path('', homePageView, name="home_page"),
    path('contact/', ContactPageView.as_view(), name="contact_page"),
    path('404', page404View, name="page404"),
    path('single-page', singlePageView, name="single_page"),
    path('news/', news_list, name="all_news_list"),
    path('news/create/', NewsCreateView.as_view(), name="news_create"),
    path('news/<slug:news>/', news_detail, name="news_detail_page"),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name="news_update"),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name="news_delete"),
    path('mahalliy/', MahalliyNewsView.as_view(), name="mahalliy_page"),
    path('xorijiy/', XorijNewsView.as_view(), name="xorijiy_page"),
    path('sport/', SportNewsView.as_view(), name="sport_page"),
    path('texnologiya/', TexnologiyaNewsView.as_view(), name="texnologiya_page"),
    path('adminpage/', admin_page_view, name="admin_page"),
    path('searchresult/', SearchResultsListView.as_view(), name="search_results"),
]
