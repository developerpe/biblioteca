import json
import ast

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse as JSR
from django.core.serializers import serialize
from django.views.generic import View

from apps.automatic_crud.generics import BaseCrud
from apps.automatic_crud.utils import get_object,get_form
from apps.automatic_crud.response_messages import *

class BaseListAJAX(BaseCrud):

    def get_queryset(self):
        return self.model.objects.filter(model_state = True)

    def get_server_side_queryset(self):
        """
        Returns the values as a dictionary ordered by the order_by attribute, 
        by default order_by = id

        """

        return self.model.objects.filter(model_state = True).values().order_by(
                                                f"{self.request.GET.get('order_by','id')}")

    def server_side(self):
        """
        Returns the paged query from the server excluding the fields that have been defined in 
        self.model.exclude_fields.

        The follow attributes must be sent in request.GET:
            start: element number where the page starts
            end: element number where the page ends

        The response structure is:

            {
                'length': # amount of records,
                'objects': # list of records
            }

        For more information see: https://www.youtube.com/watch?v=89Ur7GCyLxI

        """


        start = int(self.request.GET.get('start','0'))
        end = int(self.request.GET.get('end','10'))

        object_list = []
        
        for index,instance in enumerate(self.get_server_side_queryset()[start:start+end],start):
            for exclude_field in self.model.exclude_fields:
                del instance[f'{exclude_field}']
            
            instance['index'] = index + 1
            object_list.append(instance)   
        
        self.data = {
            'length': self.get_server_side_queryset().count(),
            'objects':object_list
        }
        self.data = json.dumps(self.data)

    def normalize_data(self):
        """
        Generate an HttpResponse instance to get the serialized query and 
        delete the ['model'] key from the dictionary and convert the dictionary 
        to json and save on self.data

        """

        temp_response = JSR({'data':self.data})
        temp_data = temp_response.content.decode("UTF-8")
        temp_data = ast.literal_eval(temp_data)
        temp_data = json.loads(temp_data['data'])
        for item in temp_data:  
            del item['model']
        self.data = json.dumps(temp_data)

    def get(self, request,model,*args,**kwargs):
        """
        Return data of model

        If self.model.server_side == True return Paginated Data
        else return No Paginated Data

        """


        self.model = model

        # login required validation
        validation_login_required,response = self.validate_login_required()
        if validation_login_required:
            return response
        
        # permission required validation
        validation_permissions,response = self.validate_permissions()
        if validation_permissions:
            return response

        if self.model.server_side:
            self.server_side()
        else:            
            self.data = serialize('json',self.get_queryset(),
                                    fields = self.get_fields_for_model(),
                                    use_natural_foreign_keys = True)
            self.normalize_data()
        return HttpResponse(self.data, content_type="application/json")

class BaseCreateAJAX(BaseCrud):
    model = None
    form_class = None

    def post(self,request,model,form = None,*args,**kwargs):
        self.model = model

        # login required validation
        validation_login_required,response = self.validate_login_required()
        if validation_login_required:
            return response
        
        # permission required validation
        validation_permissions,response = self.validate_permissions()
        if validation_permissions:
            return response
        
        self.form_class = get_form(form,self.model)
        form = self.form_class(request.POST,request.FILES)        
        if form.is_valid():
            form.save()
            return success_create_message(self.model)
        return error_create_message(self.model,form)

class BaseDetailAJAX(BaseCrud):

    def get(self,request,model,*args,**kwargs):
        self.model = model

        # login required validation
        validation_login_required,response = self.validate_login_required()
        if validation_login_required:
            return response
        
        # permission required validation
        validation_permissions,response = self.validate_permissions()
        if validation_permissions:
            return response
        
        instance = get_object(self.model,self.kwargs['pk'])        
        if instance is not None:
            self.data = serialize(
                            'json',[instance,],
                            fields = self.get_fields_for_model(),
                            use_natural_foreign_keys = True,
                            use_natural_primary_keys = True
                        )
            return HttpResponse(self.data, content_type="application/json")
        return not_found_message(self.model)

class BaseUpdateAJAX(BaseCrud):
    model = None
    form_class = None

    def post(self,request,model,form = None,*args,**kwargs):
        self.model = model        

        # login required validation
        validation_login_required,response = self.validate_login_required()
        if validation_login_required:
            return response
        
        # permission required validation
        validation_permissions,response = self.validate_permissions()
        if validation_permissions:
            return response
     
        self.form_class = get_form(form,self.model)        
        instance = get_object(self.model,self.kwargs['pk'])        
        if instance is not None:
            form = self.form_class(request.POST,request.FILES,instance = instance)            
            if form.is_valid():
                form.save()
                return success_update_message(self.model)        
            else:
                return error_update_message(self.model,form)
        return not_found_message(self.model)

class BaseDirectDeleteAJAX(BaseCrud):
    model = None

    def delete(self,request,model,*args,**kwargs):
        self.model = model

        # login required validation
        validation_login_required,response = self.validate_login_required()
        if validation_login_required:
            return response
        
        # permission required validation
        validation_permissions,response = self.validate_permissions()
        if validation_permissions:
            return response

        instance = get_object(self.model,self.kwargs['pk'])        
        if instance is not None:
            instance.delete()
            return success_delete_message(self.model)
        return not_found_message(self.model)

class BaseLogicDeleteAJAX(BaseCrud):
    model = None

    def delete(self,request,model,*args,**kwargs):
        self.model = model

        # login required validation
        validation_login_required,response = self.validate_login_required()
        if validation_login_required:
            return response
        
        # permission required validation
        validation_permissions,response = self.validate_permissions()
        if validation_permissions:
            return response

        instance = get_object(self.model,self.kwargs['pk'])        
        if instance is not None:
            self.model.objects.filter(id = self.kwargs['pk']).update(model_state = False)
            return success_delete_message(self.model)
        return not_found_message(self.model)