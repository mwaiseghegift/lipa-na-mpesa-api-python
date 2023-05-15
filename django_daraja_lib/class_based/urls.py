from .views import *
from django.urls import path

app_name = 'class_based'

urlpatterns = [
    path('stk-push/', stk_push, name='stk_push'),
    path('stk-push/query/', query_payment_status, name='stk_push_query'),
    path('callback/', c2b_callback, name='c2b_callback'),
    path('c2b/register/', register_c2b_urls, name='register_c2b_url'),
    path('c2b/validation/', validation_url, name='validation_url'),
    path('c2b/confirmation/', confirmation_url, name='confirmation_url'),
]
