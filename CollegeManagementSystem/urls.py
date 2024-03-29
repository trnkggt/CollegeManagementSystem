from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from users.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('accounts/', include('users.urls', namespace='users')),
    path('classrooms/', include('classroom.urls', namespace='classroom')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('administrator/dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('quiz/', include('quizes.urls', namespace='quizes')),
    path('', home, name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)