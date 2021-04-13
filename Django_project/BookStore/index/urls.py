from django.urls import path
from index import views
app_name = 'index'
urlpatterns=[
    path('test/',views.index_html,name='detail_hello'),
    path('redict/',views.redict_url),
    path('allbook/',views.BookName),
    path('login_page/',views.login_page),
    path('login/',views.login),
    path('search_title_form/',views.search_ttile_form),
    path('search_title/',views.serch_title),
    path('book_table/',views.book_table),

    ]

