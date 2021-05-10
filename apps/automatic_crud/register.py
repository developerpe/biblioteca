from django.apps import apps

from apps.automatic_crud.models import BaseModel

def register_models():
    """
    Register models with automatic cruds excluding models with exclude_model = True
    Return urlspatterns with automatic cruds
    """

    urlpatterns = []
    exclude_models = ['ContentType','LogEntry','Session','Permission','Group']
    models = apps.get_models()
    
    for model in models:
        
        if isinstance(model(),BaseModel):
            try:
                if model.__name__ not in exclude_models:
                    
                    if not model.exclude_model:
                        print(model.all_cruds_types)
                        if model.all_cruds_types:
                            print(model().build_generics_urls_crud())
                            urlpatterns += model().build_generics_urls_crud()
                            urlpatterns += model().build_generics_urls_ajax_crud()
                        
                        else:
                            
                            if model.ajax_crud:         
                                urlpatterns += model().build_generics_urls_ajax_crud()
                            if model.normal_cruds:
                                urlpatterns += model().build_generics_urls_crud()
            except:
                pass
    print(urlpatterns)
    return urlpatterns