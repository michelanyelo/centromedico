document.addEventListener('DOMContentLoaded', function () {
    // Manejador de eventos para el botón de agregar subespecialidad
    document.querySelector('#add-subspecialty-btn').addEventListener('click', () => {
        loadSpecialties(); // Carga las especialidades disponibles
        // Cambia la visibilidad de los formularios
        document.querySelector('#specialty-form').style.display = 'none';
        document.querySelector('#subspecialty-form').style.display = 'block';
        document.querySelector('#view-title').innerText = 'Agregar Subespecialidad';
    });

    // Manejador de eventos para el formulario de especialidad
    document.querySelector('#form-specialty').addEventListener('submit', async function (e) {
        e.preventDefault(); // Evita el envío por defecto del formulario
        const specialty_name = document.querySelector('#specialty_name').value;
        const specialty_description = document.querySelector('#specialty_description').value;

        try {
            // Envío de datos del formulario de especialidad
            const response = await fetch('', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    specialty_name: specialty_name,
                    specialty_description: specialty_description
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            await response.json(); // Espera a que la respuesta sea procesada
            loadSpecialties(); // Recarga la lista de especialidades
            // Limpia los campos del formulario
            document.querySelector('#specialty_name').value = '';
            document.querySelector('#specialty_description').value = '';
        } catch (error) {
            console.error('Error:', error); // Manejo de errores
        }
    });

    // Manejador de eventos para el formulario de subespecialidad
    document.querySelector('#form-subspecialty').addEventListener('submit', async function (e) {
        e.preventDefault(); // Evita el envío por defecto del formulario
        const specialty = document.querySelector('#specialty').value;
        const sub_name = document.querySelector('#sub_name').value;

        if (!specialty || !sub_name) {
            alert('Todos los campos son obligatorios.'); // Verifica campos vacíos
            return;
        }

        try {
            // Envío de datos del formulario de subespecialidad
            const response = await fetch('/dashboard/agregar-especialidad/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({
                    specialty: specialty,
                    sub_name: sub_name
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            await response.json(); // Espera a que la respuesta sea procesada
            // Limpia los campos del formulario y cambia la vista
            document.querySelector('#sub_name').value = '';
            document.querySelector('#specialty-form').style.display = 'block';
            document.querySelector('#subspecialty-form').style.display = 'none';
            document.querySelector('#view-title').innerText = 'Agregar Especialidad';
        } catch (error) {
            console.error('Error:', error); // Manejo de errores
        }
    });

    // Manejador de eventos para el botón de volver al formulario de especialidad
    document.querySelector('#back-to-specialty-btn').addEventListener('click', () => {
        // Cambia la visibilidad de los formularios
        document.querySelector('#specialty-form').style.display = 'block';
        document.querySelector('#subspecialty-form').style.display = 'none';
        document.querySelector('#view-title').innerText = 'Agregar Especialidad';
    });

    // Función para cargar las especialidades
    async function loadSpecialties() {
        try {
            const response = await fetch('/dashboard/listar-especialidad/');

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const specialties = await response.json();
            const specialtySelect = document.querySelector('#specialty');
            specialtySelect.innerHTML = ''; // Limpia las opciones existentes
            // Añade las nuevas opciones
            specialties.forEach((specialty) => {
                const option = document.createElement('option');
                option.value = specialty.id;
                option.innerText = specialty.nombre;
                specialtySelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching specialties:', error); // Manejo de errores
        }
    }
});
