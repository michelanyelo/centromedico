document.addEventListener('DOMContentLoaded', function () {
    const listaEspecialidades = document.querySelectorAll('#especialidades-list li');
    listaEspecialidades.forEach((especialidad) => {
        especialidad.style.display = 'none';
    });

    const letrasBtn = document.querySelectorAll('.letra-btn');
    letrasBtn.forEach((btn) => {
        btn.addEventListener('click', () => {
            const letra = btn.innerText.trim().toUpperCase();
            btn.style.backgroundColor = '#076054';
            btn.style.color = 'white';

            letrasBtn.forEach((otherBtn) => {
                if (otherBtn !== btn) {
                    otherBtn.style.backgroundColor = '';
                    otherBtn.style.color = '';
                }
            });

            filtrarEspecialidades(letra);
        });
    });

    function filtrarEspecialidades(letra) {
        listaEspecialidades.forEach((especialidad) => {
            const nombre = especialidad.innerText.trim().toUpperCase();
            if (nombre.startsWith(letra)) {
                especialidad.style.display = 'block';
            } else {
                especialidad.style.display = 'none';
            }
        });
    }
});