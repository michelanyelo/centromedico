document.addEventListener('DOMContentLoaded', function () {
    const editarButtons = document.querySelectorAll('[data-bs-toggle="modal"]');

    // Manejar el clic en los botones para abrir el modal
    editarButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const paciente = this.getAttribute('data-paciente');
            const profesionalId = this.getAttribute('data-profesional'); // ID del profesional para la reserva
            const horaInicio = this.getAttribute('data-hora_inicio');
            const horaFin = this.getAttribute('data-hora_fin');

            // Actualiza los valores del modal
            document.getElementById('modalReservaId').value = id;
            document.getElementById('modalPaciente').value = paciente;
            document.getElementById('modalHoraInicio').value = horaInicio;
            document.getElementById('modalHoraFin').value = horaFin;

            // Cargar los profesionales disponibles
            loadProfesionales(profesionalId);
        });
    });

    // Manejar el envío del formulario
    document.getElementById('formEditarReserva').addEventListener('submit', async function (event) {
        event.preventDefault();

        const id = document.getElementById('modalReservaId').value;
        // const paciente = document.getElementById('modalPaciente').value;
        const profesionalId = document.getElementById('modalProfesional').value;
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
                    profesional_id: profesionalId,
                    hora_inicio: horaInicio,
                    hora_fin: horaFin
                })
            });

            const data = await response.json();

            if (data.success) {
                alert('Reserva actualizada con éxito');
                location.reload();
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

    // Función para cargar los profesionales disponibles en el select
    async function loadProfesionales(selectedId) {
        try {
            const response = await fetch('/dashboard/listar-profesionales/');
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const profesionales = await response.json();
            const selectProfesional = document.getElementById('modalProfesional');
            selectProfesional.innerHTML = ''; // Limpia las opciones existentes
    
            profesionales.forEach((profesional) => {
                const option = document.createElement('option');
                option.value = profesional.id;
                option.textContent = `${profesional.nombre} ${profesional.apellido}`;
                if (profesional.id == selectedId) {
                    option.selected = true;
                }
                selectProfesional.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching profesionales:', error);
        }
    }
});
