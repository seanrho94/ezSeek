from django.urls import path
from .views import *
from . import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.Home, name = 'ezseek-home'),
    path('apply/<int:pk>', views.Apply, name='apply'),
    path('acceptApplicant/<int:pk>', views.AcceptApplicant, name='acceptApplicant'),
    path('rejectApplicant/<int:pk>', views.RejectApplicant, name='rejectApplicant'),
    path('jobs', JobListView.as_view(), name = 'jobs'),
    path('job/<int:pk>', JobDetailView, name='jobDetail'),
    path('myApplicant/<int:pk>', MyApplicantListView.as_view(), name='myApplicant'),
    path('companies', CompanyListView.as_view(), name = 'companies'),
    path('company/<int:pk>', CompanyDetailView.as_view(), name='companyDetail'),
    path('jobseeker/<int:pk>', JobseekerDetailView.as_view(), name='jobseekerDetail'),
    path('post/new/', PostCreateView.as_view(), name='postJob'),
    path('job/<int:pk>/update/', PostUpdateView.as_view(), name='jobUpdate'),
    path('job/<int:pk>/delete', PostDeleteView.as_view(), name='jobDelete'),
    path('myJob/<int:pk>/delete', MyJobDeleteView.as_view(), name='myJobDelete'),
    path('userJob/<str:username>', UserJobListView.as_view(), name='userJob'),
    path('myJob/<str:username>', MyJobListView.as_view(), name='myJob'),
    path('myApplication/<str:username>', MyApplicationListView.as_view(), name='myApplication'),
    path('myJobDetail/<int:pk>', MyJobDetailView.as_view(), name='myJobDetail'),
    path('register', user_views.register, name = 'register'),
    path('jsRegister', user_views.jsRegister, name = 'jsRegister'),
    path('companyRegister', user_views.companyRegister, name = 'companyRegister'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
