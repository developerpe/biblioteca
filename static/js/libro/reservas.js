function listadoLibrosReservados() {
    $.ajax({
        url: "/libro/reservas/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_libros')) {
                $('#tabla_libros').DataTable().destroy();
            }
            $('#tabla_libros tbody').html("");
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['libro'] + '</td>';
                fila += '<td>' + response[i]["fields"]['fecha_creacion'] + '</td>';
                fila += '</tr>';
                $('#tabla_libros tbody').append(fila);
            }
            $('#tabla_libros').DataTable({
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
        },
        error: function (error) {
            console.log(error);
        }
    });
}
$(document).ready(function () {
    listadoLibrosReservados();
});