const cboEspecialidad = document.getElementById("cboEspecialidad");
const cboSubEspecialidad = document.getElementById("cboSubEspecialidad");
const cboProfesional = document.getElementById("cboProfesional");
const cboHorario = document.getElementById("cboHorario");
const fechaSeleccionadaInput = document.getElementById("fechaSeleccionada");
const subespecialidadLabel = document.getElementById("subespecialidadLabel");
const horarioLabel = document.getElementById("horarioLabel");

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
            // Seleccionar automáticamente el primer profesional
            cboProfesional.selectedIndex = 0;
            // Llamar a listarHorariosDisponibles con el ID del primer profesional
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
            // Seleccionar automáticamente el primer profesional
            cboProfesional.selectedIndex = 0;
            // Llamar a listarHorariosDisponibles con el ID del primer profesional
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

        let opciones = "";
        if (data.message === "Success") {
            data.horarios.forEach((horario) => {
                // Convertir la fecha a un objeto Date con la zona horaria de Santiago
                const fecha = new Date(`${horario.fecha}T00:00:00`);
                const timezoneLocal = { timeZone: 'America/Santiago' };
                fecha.toLocaleString("es-ES", timezoneLocal); // Establecer la zona horaria
                // Obtener el nombre del día de la semana
                const diaSemana = fecha.toLocaleDateString("es-ES", { weekday: "long" });
                const diaSemanaCapitalizado = diaSemana.charAt(0).toUpperCase() + diaSemana.slice(1);
                // Obtener el número del día en el calendario
                const numeroDia = fecha.getDate();
                if (fecha.getMonth() + 1 < 10) {
                    mes_completo = "0" + (fecha.getMonth() + 1)
                } else {
                    mes_completo = fecha.getMonth() + 1
                }

                if (numeroDia < 10) {
                    dia_completo = "0" + (numeroDia)
                } else {
                    dia_completo = numeroDia
                }
                opciones += `<option value="${horario.id}" data-fecha="${dia_completo}/${mes_completo}/${fecha.getFullYear()}/${horario.hora_inicio}/${horario.hora_fin}">${diaSemanaCapitalizado} ${dia_completo}/${mes_completo}/${fecha.getFullYear()} : ${horario.hora_inicio} - ${horario.hora_fin}</option>`;
            });
            cboHorario.innerHTML = ""; // Limpiar las opciones existentes
            cboHorario.innerHTML = opciones; // Agregar las nuevas opciones
            cboHorario.selectedIndex = 0; // Establecer la primera opción como seleccionada
            cboHorario.dispatchEvent(new Event("change")); // Disparar manualmente el evento change
        } else {
            opciones = '<option value="0">No hay horarios disponibles</option>';
            cboHorario.innerHTML = opciones; // Limpiar el campo de selección de horarios y establecer el mensaje de "No hay horarios disponibles"
        }
        cboHorario.style.display = "block";
        horarioLabel.style.display = "block";
    } catch (error) {
        console.error("Error al obtener los horarios disponibles:", error);
    }
};


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
            // Si se selecciona "No hay horarios disponibles", mostrar un mensaje de error
            alert("Por favor, seleccione un horario disponible.");
            // Reiniciar el campo de selección de horarios seleccionando la primera opción disponible
            cboHorario.selectedIndex = 0;
        } else {
            // Si se selecciona un horario disponible, continuar con el proceso
            const fechaSeleccionada = cboHorario.options[cboHorario.selectedIndex].getAttribute("data-fecha");
            const [dia, mes, anio, hora_inicio, hora_fin] = fechaSeleccionada.split('/');
            document.getElementById("dia").value = dia;
            document.getElementById("mes").value = mes;
            document.getElementById("anio").value = anio;
            document.getElementById("hora_inicio").value = hora_inicio;
            document.getElementById("hora_fin").value = hora_fin;
            
        }
    });
};


window.addEventListener("load", async () => {
    await cargaInicial();
});


document.getElementById("agendarForm").addEventListener("submit", function (event) {
    if (!validarFormulario()) {
        event.preventDefault(); // Evita que el formulario se envíe si la validación falla
    }
});

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
        return false; // Evita que el formulario se envíe si hay campos no válidos
    }

    // Si todos los campos tienen selecciones válidas, el formulario puede enviarse
    return true;
};
