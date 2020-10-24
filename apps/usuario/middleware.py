import datetime
from datetime import timedelta
from apps.libro.models import Reserva

class PruebaMiddleware:
    
    def __init__(self,get_response):        
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)
        return response

    def process_view(self,request,view_func,view_args,view_kwargs):
        if request.user.is_authenticated:
            fecha_actual = datetime.date.today()
            reservas = Reserva.objects.filter(estado = True,usuario = request.user)
            for reserva in reservas:
                fecha_vencimiento = reserva.fecha_creacion + timedelta(days = 7)
                if fecha_actual > fecha_vencimiento:
                    reserva.estado = False
                    reserva.save()