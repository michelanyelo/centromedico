document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#add-subspecialty-btn').addEventListener('click', () => {
        loadSpecialties();
        document.querySelector('#specialty-form').style.display = 'none';
        document.querySelector('#subspecialty-form').style.display = 'block';
        document.querySelector('#view-title').innerText = 'Agregar Subespecialidad';
    });

    document.querySelector('#form-specialty').addEventListener('submit', function (e) {
        e.preventDefault();
        const specialty_name = document.querySelector('#specialty_name').value;
        const specialty_description = document.querySelector('#specialty_description').value;

        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams({
                specialty_name: specialty_name,
                specialty_description: specialty_description
            })
        })
            .then((response) => response.json())
            .then(() => {
                loadSpecialties();
                document.querySelector('#specialty_name').value = '';
                document.querySelector('#specialty_description').value = ''; // Clear description field
            });
    });

    document.querySelector('#form-subspecialty').addEventListener('submit', function (e) {
        e.preventDefault();
        const specialty = document.querySelector('#specialty').value;
        const sub_name = document.querySelector('#sub_name').value;

        if (!specialty || !sub_name) {
            alert('Todos los campos son obligatorios.');
            return;
        }

        fetch('/dashboard/agregar-especialidad/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: new URLSearchParams({
                specialty: specialty,
                sub_name: sub_name
            })
        })
            .then((response) => response.json())
            .then(() => {
                document.querySelector('#sub_name').value = '';
                document.querySelector('#specialty-form').style.display = 'block';
                document.querySelector('#subspecialty-form').style.display = 'none';
                document.querySelector('#view-title').innerText = 'Agregar Especialidad';
            })
            .catch((error) => console.error('Error:', error));
    });

    document.querySelector('#back-to-specialty-btn').addEventListener('click', () => {
        document.querySelector('#specialty-form').style.display = 'block';
        document.querySelector('#subspecialty-form').style.display = 'none';
        document.querySelector('#view-title').innerText = 'Agregar Especialidad';
    });

    function loadSpecialties() {
        fetch('/dashboard/listar-especialidad/')
            .then((response) => response.json())
            .then((specialties) => {
                const specialtySelect = document.querySelector('#specialty');
                specialtySelect.innerHTML = '';
                specialties.forEach((specialty) => {
                    const option = document.createElement('option');
                    option.value = specialty.id;
                    option.innerText = specialty.nombre; // Asegúrate de usar el nombre correcto
                    specialtySelect.appendChild(option);
                });
            })
            .catch((error) => console.error('Error fetching specialties:', error));
    }
});
