from django.http import JsonResponse as JSR
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.views.generic import View

class BaseCrudMixin(AccessMixin):
    model = None
    data = None
    permission_required = ()

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(self.__class__.__name__)
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def set_permissions(self):
        """
        Set permission_required with default permissions if default_permissions = True
        """

        if self.model.default_permissions:
            __default_permissions = ('add_{0}'.format(self.model.__name__.lower()),
                                    'view_{0}'.format(self.model.__name__.lower()),
                                    'delete_{0}'.format(self.model.__name__.lower()),
                                    'change_{0}'.format(self.model.__name__.lower()))
            self.permission_required = __default_permissions
        else:
            self.permission_required = self.model.permission_required

    def validate_permissions(self,*args, **kwargs):
        """
        Validate permissions required if model_permissions = True
        """

        if self.model.model_permissions:
            self.set_permissions()
            if not self.has_permission() and not self.request.user.is_superuser:
                response = JSR({'error': 'No tiene los permisos para realizar esta acción.'})
                response.status_code = 403
                return True,response
        return False,None

    def validate_login_required(self, *args, **kwargs):
        """
        Validate login required if login_required = True
        """
        
        if self.model.login_required:          
            if not self.request.user.is_authenticated:
                response = JSR({'error': 'No ha iniciado sesión.'})
                response.status_code = 403
                return True,response
        return False,None


class BaseCrud(BaseCrudMixin,View):

    def get_fields_for_model(self):
        """
        Return fields for model excluding exclude_fields of model
        """
        fields = [field.name for field in self.model._meta.get_fields()]
        for field in self.model.exclude_fields:            
            if field in fields:
                fields.remove(field)
        return fields