$(document).ready(function () {
    // Ocultar las especialidades al cargar la página
    $('#especialidades-list li').hide();

    // Manejar el clic en los botones de letras
    $('.letra-btn').click(function () {
        var letra = $(this).text().trim().toUpperCase();
        $(this).css({ 'background-color': '#076054', 'color': 'white' })
            .siblings().css({ 'background-color': '', 'color': '' });

        filtrarEspecialidades(letra);
    });

    // Función para filtrar las especialidades según la letra seleccionada
    function filtrarEspecialidades(letra) {
        $('#especialidades-list li').each(function () {
            var nombre = $(this).text().trim().toUpperCase();
            $(this).toggle(nombre.startsWith(letra));
        });
    }

    $('#especialidad').change(function () {
        var especialidad = $(this).val();
        $.ajax({
            url: '/reservas/obtener-subespecialidades/',
            data: { 'especialidad_id': especialidad }, 
            dataType: 'json',
            success: function (data) {
                var options = '<option value="">Seleccione...</option>';
                for (var i = 0; i < data.length; i++) {
                    options += '<option value="' + data[i].id + '">' + data[i].nombre + '</option>'; 
                }
                $('#subespecialidad').html(options);
            }
        });
    });

});
