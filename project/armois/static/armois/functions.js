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
});
