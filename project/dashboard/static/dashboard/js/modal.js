document.addEventListener('DOMContentLoaded', function () {
    const editarButtons = document.querySelectorAll('[data-bs-toggle="modal"]');

    // Manejar el clic en los botones para abrir el modal
    editarButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const paciente = this.getAttribute('data-paciente');
            const profesionalId = this.getAttribute('data-profesional'); // ID del profesional para la reserva
            const horarioId = this.getAttribute('data-horario'); // ID del horario para la reserva

            // Actualiza los valores del modal
            document.getElementById('modalReservaId').value = id;
            document.getElementById('modalPaciente').value = paciente;

            // Cargar los profesionales disponibles y seleccionar el actual
            loadProfesionales(profesionalId);

            // Cargar los horarios disponibles para el profesional seleccionado
            loadHorariosDisponibles(profesionalId, horarioId);
        });
    });

    // Manejar el envío del formulario
    document.getElementById('formEditarReserva').addEventListener('submit', async function (event) {
        event.preventDefault();

        const id = document.getElementById('modalReservaId').value;
        const profesionalId = document.getElementById('modalProfesional').value;
        const horarioId = document.getElementById('modalHorario').value;

        try {
            const response = await fetch('/dashboard/editar-reserva/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    id: id,
                    profesional_id: profesionalId,
                    horario_id: horarioId
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

            // Asegúrate de que al cambiar el profesional, se actualicen los horarios
            selectProfesional.addEventListener('change', function () {
                const selectedProfesionalId = this.value;
                loadHorariosDisponibles(selectedProfesionalId);
            });

            // Forzar la carga de horarios para el profesional actualmente seleccionado
            if (selectedId) {
                loadHorariosDisponibles(selectedId);
            }
        } catch (error) {
            console.error('Error fetching profesionales:', error);
        }
    }

    // Función para cargar los horarios disponibles del profesional seleccionado
    async function loadHorariosDisponibles(profesionalId, selectedHorarioId) {
        try {
            const response = await fetch(`/dashboard/listar-horarios/${profesionalId}/`);

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const horarios = await response.json();
            const selectHorario = document.getElementById('modalHorario');
            selectHorario.innerHTML = ''; // Limpia las opciones existentes

            horarios.forEach((horario) => {
                const option = document.createElement('option');
                option.value = horario.id;
                option.textContent = `${horario.hora_inicio} - ${horario.hora_fin}`;
                if (horario.id == selectedHorarioId) {
                    option.selected = true;
                }
                selectHorario.appendChild(option);
            });

            // Asegúrate de que el horario seleccionado esté visible
            if (selectedHorarioId) {
                selectHorario.value = selectedHorarioId;
            }
        } catch (error) {
            console.error('Error fetching horarios:', error);
        }
    }
});
