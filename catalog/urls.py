from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shoes/', views.ShoeListView.as_view(), name='shoes'),
    path('shoes/<int:pk>', views.ShoeDetailView.as_view(), name='shoe-detail'),
    path('brands/', views.BrandListView.as_view(), name = 'brands'),
    path('brands/<int:brand_id>', views.brand_detail_view, name = 'brand-detail'),
    path('reports/', views.Reports.as_view(), name = 'reports'),
    path('report_results/', views.report_results, name='report_results'),

]
