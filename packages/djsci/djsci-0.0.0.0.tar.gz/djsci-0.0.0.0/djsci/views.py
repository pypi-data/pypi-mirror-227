from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
import nbconvert
import nbformat
from nbformat.notebooknode import NotebookNode

from djsci.models import PrivateFile


def api_root(request: HttpRequest) -> JsonResponse:

    return JsonResponse('djsci_api_root', safe=False)


def sync_get_file(name_id: str) -> bytes:

    try:
        private_file = PrivateFile.objects.get(name=name_id).file
    except:
        private_file = PrivateFile.objects.get(id=name_id).file

    with private_file.open() as open_file:
        sync_file = open_file.read()

    return sync_file


def convert_ipynb_to_python(sync_file: bytes) -> str:

    notebook_node = nbformat.reads(sync_file, as_version=4)

    notebook_python = nbconvert.PythonExporter().from_notebook_node(notebook_node)[0]

    return notebook_python


def sync_exec(request: HttpRequest, sync_file: bytes | str) -> (
    # not sure how else to allow any json :
    dict | list | str | int | float | bool | None
):
    # not sure why locals() doesn't work :
    exec(sync_file, globals())#, locals())

    return djsci_handler(request=request)


def sync_py(request: HttpRequest, name_id: str) -> JsonResponse:

    sync_file = sync_get_file(name_id)

    djsci_handler_result = sync_exec(request, sync_file)
    
    return JsonResponse(djsci_handler_result, safe=False)


def sync_ipynb(request: HttpRequest, name_id: str) -> JsonResponse:

    sync_file = sync_get_file(name_id)

    notebook_python = convert_ipynb_to_python(sync_file)

    djsci_handler_result = sync_exec(request, notebook_python)
    
    return JsonResponse(djsci_handler_result, safe=False)
