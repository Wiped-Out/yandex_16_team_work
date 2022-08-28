import mimetypes

import debug_toolbar
from django.contrib import admin
from django.urls import include, path

mimetypes.add_type('application/javascript', '.js', True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/', include('movies.api.urls')),
]
