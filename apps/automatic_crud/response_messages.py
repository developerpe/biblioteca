from django.http import JsonResponse as JR

from apps.automatic_crud.data_types import Instance,JsonResponse,DjangoForm

def jr_response(message:str,error: str,statud_code: int) -> JsonResponse:
    response = JR({'message':message,'error':error})
    response.status_code = statud_code
    return response

def success_create_message(model: Instance) -> JsonResponse:
    message = model().build_message(model.success_create_message)
    error = 'Ninguno'
    return jr_response(message,error,201)

def error_create_message(model: Instance, form:DjangoForm) -> JsonResponse:
    message = model().build_message(model.error_create_message)
    error = form.errors
    return jr_response(message,error,400)

def success_update_message(model: Instance) -> JsonResponse:
    message = model().build_message(model.success_update_message)
    error = 'Ninguno'
    return jr_response(message,error,200)

def error_update_message(model: Instance, form:DjangoForm) -> JsonResponse:
    message = model().build_message(model.error_update_message)
    error = form.errors
    return jr_response(message,error,400)

def success_delete_message(model: Instance) -> JsonResponse:
    message = model().build_message(model.success_delete_message)
    error = 'Ninguno'
    return jr_response(message,error,200)

def not_found_message(model: Instance) -> JsonResponse:
    response = JR({'error':model.non_found_message})
    response.status_code = 400
    return response