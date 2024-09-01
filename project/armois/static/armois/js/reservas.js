// Funciones de carga de datos

const listarEspecialidad = async () => {
    try {
        const response = await fetch("./especialidades");
        const data = await response.json();
        if (data.message === "Success") {
            let opciones = cboEspecialidad.innerHTML;
            data.especialidad.forEach((especialidad) => {
                opciones += `<option value="${especialidad.id}">${especialidad.nombre}</option>`;
            });
            cboEspecialidad.innerHTML = opciones;
            listarSubEspecialidad(data.especialidad[0].id);
        } else {
            alert("Especialidad no encontrada");
        }
    } catch (error) {
        console.error("Error al obtener las especialidades:", error);
    }
};

const listarSubEspecialidad = async (idEspecialidad) => {
    try {
        const response = await fetch(`./subespecialidades/${idEspecialidad}`);
        const data = await response.json();

        if (data.message === "Success") {
            let opciones = "";
            data.subespecialidad.forEach((subespecialidad) => {
                opciones += `<option value="${subespecialidad.id}">${subespecialidad.nombre}</option>`;
            });
            cboSubEspecialidad.innerHTML = opciones;
            cboSubEspecialidad.style.display = "block";
            subespecialidadLabel.style.display = "block";
            listarProfesionalesConSubesp(data.subespecialidad[0].id);
        } else {
            cboProfesional.innerHTML = '<option value="0">No hay profesional</option>';
            cboHorario.innerHTML = '<option value="0">No hay horarios disponibles</option>';
            cboSubEspecialidad.style.display = "none";
            subespecialidadLabel.style.display = "none";
        }
    } catch (error) {
        console.error("Error al obtener las subespecialidades:", error);
    }
};

const listarProfesionalesConSubesp = async (idSubEspecialidad) => {
    try {
        const response = await fetch(`./profesionales-con-subesp/${idSubEspecialidad}`);
        const data = await response.json();

        if (data.message === "Success") {
            let opciones = "";
            data.profesional_subesp.forEach((profesional) => {
                opciones += `<option value="${profesional.id}">${profesional.nombre} ${profesional.apellido}</option>`;
            });
            cboProfesional.innerHTML = opciones;
            cboProfesional.selectedIndex = 0;
            listarHorariosDisponibles(cboProfesional.value);
        } else {
            let opciones = `<option value="0">No hay profesional</option>`;
            cboProfesional.innerHTML = opciones;
        }
    } catch (error) {
        console.error("Error al obtener los profesionales con subespecialidad:", error);
    }
};

const listarProfesionalesSinSubesp = async (idEspecialidad) => {
    try {
        const response = await fetch(`./profesionales-sin-subesp/${idEspecialidad}`);
        const data = await response.json();

        if (data.message === "Success") {
            let opciones = "";
            data.profesionales_sin_subesp.forEach((profesional) => {
                opciones += `<option value="${profesional.id}">${profesional.nombre} ${profesional.apellido}</option>`;
            });
            cboProfesional.innerHTML = opciones;
            cboProfesional.selectedIndex = 0;
            listarHorariosDisponibles(cboProfesional.value);
        } else {
            let opciones = `<option value="0">No hay profesional</option>`;
            cboProfesional.innerHTML = opciones;
        }
    } catch (error) {
        console.error("Error al obtener los profesionales sin subespecialidad:", error);
    }
};

const listarHorariosDisponibles = async (profesionalId) => {
    try {
        const response = await fetch(`./horarios/${profesionalId}`);
        const data = await response.json();

        let opciones = data.message === "Success"
            ? data.horarios.map(horario => {
                const fechaFormateada = formatearFecha(horario.fecha);
                return `<option value="${horario.id}" data-fecha="${fechaFormateada}" data-hora_inicio="${horario.hora_inicio}" data-hora_fin="${horario.hora_fin}">${fechaFormateada} : ${horario.hora_inicio} - ${horario.hora_fin}</option>`;
            }).join("")
            : '<option value="0">No hay horarios disponibles</option>';

        cboHorario.innerHTML = opciones;
        cboHorario.selectedIndex = 0;
        cboHorario.dispatchEvent(new Event("change"));
        cboHorario.style.display = "block";
        horarioLabel.style.display = "block";
    } catch (error) {
        console.error("Error al obtener los horarios disponibles:", error);
    }
};


// Funciones de manipulación de UI

const cargaInicial = async () => {
    await listarEspecialidad();

    cboEspecialidad.addEventListener("change", () => {
        listarSubEspecialidad(cboEspecialidad.value);
        listarProfesionalesSinSubesp(cboEspecialidad.value);
    });

    cboSubEspecialidad.addEventListener("change", () => {
        listarProfesionalesConSubesp(cboSubEspecialidad.value);
    });

    cboProfesional.addEventListener("change", () => {
        listarHorariosDisponibles(cboProfesional.value);
    });

    cboHorario.addEventListener("change", () => {
        if (cboHorario.value === "0") {
            alert("Por favor, seleccione un horario disponible.");
            cboHorario.selectedIndex = 0;
        } else {
            const fechaSeleccionada = cboHorario.options[cboHorario.selectedIndex].getAttribute("data-fecha");
            const [dia, mes, anio] = fechaSeleccionada.split('/');
            document.getElementById("dia").value = dia;
            document.getElementById("mes").value = mes;
            document.getElementById("anio").value = anio;
            alert(dia);
            
            const hora_inicio = cboHorario.options[cboHorario.selectedIndex].getAttribute("data-hora_inicio");
            const hora_fin = cboHorario.options[cboHorario.selectedIndex].getAttribute("data-hora_fin");
            document.getElementById("hora_inicio").value = hora_inicio;
            document.getElementById("hora_fin").value = hora_fin;
        }
    });
    
};

// Valida el formulario antes de enviarlo
const validarFormulario = () => {
    const especialidadSeleccionada = cboEspecialidad.value;
    const subEspecialidadSeleccionada = cboSubEspecialidad.value;
    const profesionalSeleccionado = cboProfesional.value;
    const horarioSeleccionado = cboHorario.value;

    if (
        especialidadSeleccionada === "0" ||
        subEspecialidadSeleccionada === "0" ||
        profesionalSeleccionado === "0" ||
        horarioSeleccionado === "0"
    ) {
        alert("Por favor, complete todos los campos antes de enviar el formulario.");
        return false;
    }

    return true;
};

// Formatea la fecha en el formato deseado
// Formatea la fecha en el formato deseado
const formatearFecha = (fechaStr) => {
    const fecha = new Date(`${fechaStr}T00:00:00`);
    const opciones = {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        timeZone: "America/Santiago"
    };
    return fecha.toLocaleDateString("es-ES", opciones);
};


// Inicializa la página y los eventos
window.addEventListener("load", async () => {
    await cargaInicial();
});

// Maneja el evento de envío del formulario
document.getElementById("agendarForm").addEventListener("submit", function (event) {
    if (!validarFormulario()) {
        event.preventDefault();
    }
});
