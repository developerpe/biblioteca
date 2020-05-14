function listadoUsuarios(){
    $.ajax({
        url: "/usuarios/listado_usuarios/",
        type: "get",
        dataType: "json",
        success: function(response){
            if($.fn.DataTable.isDataTable('#tabla_usuarios')){
                $('#tabla_usuarios').DataTable().destroy();
            }
            $("#tabla_usuarios tbody").html("");
            for(let i = 0; i  < response.length;i++){
                let fila = '<tr class = "text-center">';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['username'] + '</td>';
                fila += '<td>' + response[i]["fields"]['nombres'] + '</td>';
                fila += '<td>' + response[i]["fields"]['apellidos'] + '</td>';
                fila += '<td><button> EDITAR </button> <button> ELIMINAR </button><td>';
                fila += '</tr>';
                $('#tabla_usuarios tbody').append(fila);
            }
            $("#tabla_usuarios").DataTable({
                language: {
                    "decimal": "",
                    "emptyTable": "No hay información",
                    "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
                    "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                    "infoPostFix": "",
                    "thousands": ",",
                    "lengthMenu": "Mostrar _MENU_ Entradas",
                    "loadingRecords": "Cargando...",
                    "processing": "Procesando...",
                    "search": "Buscar:",
                    "zeroRecords": "Sin resultados encontrados",
                    "paginate": {
                        "first": "Primero",
                        "last": "Ultimo",
                        "next": "Siguiente",
                        "previous": "Anterior"
                    },
                },
            });
        }
    })
}

$(document).ready(function(){    
    listadoUsuarios();
});