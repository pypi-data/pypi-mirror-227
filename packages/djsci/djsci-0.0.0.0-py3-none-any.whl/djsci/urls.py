from django.urls import path, re_path
from django.views.static import serve
from django.contrib.auth.decorators import login_required

from djsci import views


DJSCI_API_ROOT = 'djsci'


djsci_urls = [
    re_path(fr'{DJSCI_API_ROOT}/?$', views.api_root, name="api_root"),
    re_path(fr'{DJSCI_API_ROOT}/sync_py/(?P<name_id>\w+)/?$', login_required(views.sync_py), name="sync_py"),
    re_path(fr'{DJSCI_API_ROOT}/sync_ipynb/(?P<name_id>\w+)/?$', login_required(views.sync_ipynb), name="sync_ipynb"),
    re_path(
        r'^private_files/(?P<path>.*)$',
        serve,
        {'document_root': 'private_files'},
    ),
]
