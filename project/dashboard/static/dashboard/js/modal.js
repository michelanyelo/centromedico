document.addEventListener('DOMContentLoaded', function () {
    const editarButtons = document.querySelectorAll('[data-bs-toggle="modal"]');

    editarButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const paciente = this.getAttribute('data-paciente');
            const profesional = this.getAttribute('data-profesional');
            const horaInicio = this.getAttribute('data-hora_inicio');
            const horaFin = this.getAttribute('data-hora_fin');

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

        const id = document.getElementById('modalReservaId').value;
        // const paciente = document.getElementById('modalPaciente').value
        // const profesional = document.getElementById('modalProfesional').value
        const horaInicio = document.getElementById('modalHoraInicio').value;
        const horaFin = document.getElementById('modalHoraFin').value;

        try {
            const response = await fetch('/dashboard/editar-reserva/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    id: id,
                    // paciente: paciente,
                    // profesional: profesional,
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
