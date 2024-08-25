document.addEventListener('DOMContentLoaded', function () {
    let editarButtons = document.querySelectorAll('[data-bs-toggle="modal"]');

    editarButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            let id = this.getAttribute('data-id');
            let paciente = this.getAttribute('data-paciente');
            let profesional = this.getAttribute('data-profesional');
            let horaInicio = this.getAttribute('data-hora_inicio');
            let horaFin = this.getAttribute('data-hora_fin');

            // Verifica que los valores se obtienen correctamente
            console.log('ID:', id);
            console.log('Paciente:', paciente);
            console.log('Profesional:', profesional);
            console.log('Hora Inicio:', horaInicio);
            console.log('Hora Fin:', horaFin);

            // Actualiza los valores del modal
            document.getElementById('modalReservaId').value = id;
            document.getElementById('modalPaciente').value = paciente;
            document.getElementById('modalProfesional').value = profesional;
            document.getElementById('modalHoraInicio').value = horaInicio;
            document.getElementById('modalHoraFin').value = horaFin;
        });
    });

    document.getElementById('formEditarReserva').addEventListener('submit', async function (event) {
        event.preventDefault(); // Evita el envío por defecto del formulario

        let id = document.getElementById('modalReservaId').value;
        let horaInicio = document.getElementById('modalHoraInicio').value;
        let horaFin = document.getElementById('modalHoraFin').value;

        try {
            const response = await fetch('/dashboard/editar-reserva', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    id: id,
                    hora_inicio: horaInicio,
                    hora_fin: horaFin
                })
            });

            const data = await response.json();

            if (data.success) {
                alert('Reserva actualizada con éxito');
                location.reload(); // Recarga la lista de reservas
            } else {
                alert('Error al actualizar la reserva: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un problema con la solicitud. Por favor, inténtalo de nuevo.');
        }
    });

    // Función para obtener el token CSRF
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
