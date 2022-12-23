from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),
]

handler404 = 'game.views.page404.error_404'
handler500 = 'game.views.page500.error_500'
