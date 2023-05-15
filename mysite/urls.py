from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),
]

handler404 = 'game.views.error.error_404'
handler500 = 'game.views.error.error_500'
