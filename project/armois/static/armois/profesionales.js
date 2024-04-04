const handleJSONResponse = async (response) => {
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.message || response.statusText);
    }
    return data;
};

const generarOpcionesSelect = (items) => {
    return items.map((item) => `<option value="${item.id}">${item.nombre}</option>`).join('');
};

const listarEspecialidad = async () => {
    try {
        const response = await fetch("./especialidades");
        const data = await handleJSONResponse(response);

        especialidadId.innerHTML = generarOpcionesSelect(data.especialidad);
        listarSubEspecialidad(data.especialidad[0].id);
    } catch (error) {
        console.error("Error al obtener las especialidades:", error);
        alert("Error al obtener las especialidades");
    }
};

const listarSubEspecialidad = async (idEspecialidad) => {
    try {
        const response = await fetch(`./subespecialidades/${idEspecialidad}`);
        const data = await handleJSONResponse(response);

        cboSubEspecialidad.innerHTML = generarOpcionesSelect(data.subespecialidad);
        if (data.subespecialidad.length > 0) {
            listarProfesionalesConSubesp(data.subespecialidad[0].id);
        } else {
            cboProfesional.innerHTML = '<option value="notfound">No hay profesional</option>';
        }
    } catch (error) {
        console.error("Error al obtener las subespecialidades:", error);
        alert("Error al obtener las subespecialidades");
    }
};

const listarProfesionalesConSubesp = async (idSubEspecialidad) => {
    try {
        const response = await fetch(`./profesionales/${idSubEspecialidad}`);
        const data = await handleJSONResponse(response);

        cboProfesional.innerHTML = generarOpcionesSelect(data.profesional_subesp);
    } catch (error) {
        console.error("Error al obtener los profesionales con subespecialidad:", error);
        alert("Error al obtener los profesionales con subespecialidad");
    }
};

const listarProfesionalesSinSubesp = async (idEspecialidad) => {
    try {
        const response = await fetch(`./profesionales-sin-subesp/${idEspecialidad}`);
        const data = await handleJSONResponse(response);

        cboProfesional.innerHTML = generarOpcionesSelect(data.profesionales_sin_subesp);
    } catch (error) {
        console.error("Error al obtener los profesionales sin subespecialidad:", error);
        alert("Error al obtener los profesionales sin subespecialidad");
    }
};

const cargaInicial = async () => {
    await listarEspecialidad();

    especialidadId.addEventListener("change", () => {
        const especialidadIdSeleccionada = especialidadId.value;
        listarSubEspecialidad(especialidadIdSeleccionada);
        listarProfesionalesSinSubesp(especialidadIdSeleccionada);
    });

    cboSubEspecialidad.addEventListener("change", () => {
        listarProfesionalesConSubesp(cboSubEspecialidad.value);
    });
};

window.addEventListener("load", async () => {
    await cargaInicial();
});
