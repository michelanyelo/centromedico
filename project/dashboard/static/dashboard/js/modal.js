// Funciones de carga de datos

const listarProfesionalesModal = async (profesionalId, especialidadId, horarioId) => {
    try {
        const response = await fetch('./listar-profesionales/');
        const data = await response.json();

        let opciones = data.length > 0
            ? data.map(profesional => `<option value="${profesional.id}">${profesional.nombre} ${profesional.apellido}</option>`).join("")
            : '<option value="0">No hay profesionales disponibles</option>';

        modalProfesional.innerHTML = opciones;
        modalProfesional.value = profesionalId;

        listarEspecialidadesModal(profesionalId, especialidadId, horarioId);
    } catch (error) {
        console.error("Error al obtener los profesionales:", error);
    }
};

const listarEspecialidadesModal = async (profesionalId, especialidadId, horarioId) => {
    try {
        const response = await fetch(`./listar-especialidad/${profesionalId}`);
        const data = await response.json();

        if (data.success) {
            const especialidad = data.especialidad;
            const opciones = especialidad
                ? `<option value="${especialidad.id}">${especialidad.nombre}</option>`
                : '<option value="0">No hay especialidades disponibles</option>';

            modalEspecialidad.innerHTML = opciones;
            modalEspecialidad.value = especialidadId;

            listarSubespecialidadesModal(especialidadId);
            listarHorariosModal(profesionalId, horarioId);
        } else {
            alert("Especialidades no encontradas");
        }
    } catch (error) {
        console.error("Error al obtener las especialidades:", error);
    }
};

const listarSubespecialidadesModal = async (especialidadId) => {
    try {
        const response = await fetch(`./listar-subespecialidades/${especialidadId}`);
        const data = await response.json();

        if (data.success) {
            const opciones = data.subespecialidades.length > 0
                ? data.subespecialidades.map(subespecialidad => `<option value="${subespecialidad.id}">${subespecialidad.nombre}</option>`).join("")
                : '<option value="0">No hay subespecialidades disponibles</option>';

            modalSubespecialidad.innerHTML = opciones;
            modalSubespecialidad.style.display = "block";
        } else {
            modalSubespecialidad.innerHTML = '<option value="0">No hay subespecialidades disponibles</option>';
            modalSubespecialidad.style.display = "none";
        }
    } catch (error) {
        console.error("Error al obtener las subespecialidades:", error);
        modalSubespecialidad.innerHTML = '<option value="0">Error al cargar subespecialidades</option>';
        modalSubespecialidad.style.display = "none";
    }
};

const listarHorariosModal = async (profesionalId, horarioId) => {
    try {
        const response = await fetch(`./listar-horarios/${profesionalId}/`);
        const data = await response.json();

        const opciones = data.length > 0
            ? data.map(horario => {
                const fechaFormateada = formatearFecha(horario.fecha);
                return `<option value="${horario.id}">${fechaFormateada} ${horario.hora_inicio} - ${horario.hora_fin}</option>`;
            }).join("")
            : '<option value="0">No hay horarios disponibles</option>';

        modalHorario.innerHTML = opciones;
        modalHorario.value = horarioId;
    } catch (error) {
        console.error("Error al obtener los horarios disponibles:", error);
    }
};

// Función para darle legibilidad a la fecha
const formatearFecha = (fechaStr) => {
    const fecha = new Date(fechaStr + 'T00:00:00');
    const opcionesFecha = {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        timeZone: 'America/Santiago'
    };
    return fecha.toLocaleDateString('es-ES', opcionesFecha);
};

// Manejo del evento para mostrar el modal
document.getElementById('editarReserva').addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const reservaId = button.getAttribute('data-reserva-id');
    const pacienteNombre = button.getAttribute('data-paciente-nombre');
    const profesionalId = button.getAttribute('data-profesional-id');
    const especialidadId = button.getAttribute('data-especialidad-id');
    const horarioId = button.getAttribute('data-horario-id');

    modalReservaId.value = reservaId;
    modalPaciente.value = pacienteNombre;

    listarProfesionalesModal(profesionalId, especialidadId, horarioId);
});

// Actualizar especialidades cuando cambie el profesional
modalProfesional.addEventListener("change", () => {
    listarEspecialidadesModal(modalProfesional.value, null, null);
});

// Actualizar subespecialidades cuando cambie la especialidad
modalEspecialidad.addEventListener("change", () => {
    listarSubespecialidadesModal(modalEspecialidad.value);
});

// Actualizar horarios cuando cambie la subespecialidad
modalSubespecialidad.addEventListener("change", () => {
    listarHorariosModal(modalProfesional.value, null);
});

// Validar el formulario antes de enviarlo
formEditarReserva.addEventListener('submit', async function (event) {
    event.preventDefault();

    const profesional = modalProfesional.value;
    const especialidad = modalEspecialidad.value;
    const subespecialidad = modalSubespecialidad.value;
    const horario = modalHorario.value;
    const reservaId = modalReservaId.value;

    if (!profesional || profesional === "0") {
        alert('Por favor, seleccione un profesional.');
        return;
    }
    if (!especialidad || especialidad === "0") {
        alert('Por favor, seleccione una especialidad.');
        return;
    }
    if (!horario || horario === "0") {
        alert('Por favor, seleccione un horario.');
        return;
    }

    try {
        const response = await fetch('editar-reserva/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                id: reservaId,
                profesional_id: profesional,
                especialidad_id: especialidad,
                subespecialidad_id: subespecialidad,
                horario_id: horario
            })
        });

        const result = await response.json();
        if (result.success) {
            alert('Reserva actualizada exitosamente');
            $('#editarReserva').modal('hide');
            location.reload();
        } else {
            alert('Error al actualizar la reserva: ' + result.error);
        }
    } catch (error) {
        console.error('Error al actualizar la reserva:', error);
        alert('Error al actualizar la reserva.');
    }
});

// Función para finalizar una reserva
const finalizarReserva = async (reservaId) => {
    if (confirm('¿Estás seguro de que deseas finalizar esta reserva?')) {
        try {
            const response = await fetch('./finalizar-reserva/', { // Actualiza el endpoint según tu implementación
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ id: reservaId })
            });

            const result = await response.json();
            if (result.success) {
                alert('Reserva finalizada exitosamente');
                location.reload();
            } else {
                alert('Error al finalizar la reserva: ' + result.error);
            }
        } catch (error) {
            console.error('Error al finalizar la reserva:', error);
            alert('Error al finalizar la reserva.');
        }
    }
};
