# Capstone Project / Centro Médico - Citas

## Descripción

Este proyecto es una aplicación web dinámica desarrollada con Django en el backend y JavaScript en el frontend. La aplicación está diseñada para gestionar reservas, con integración de funcionalidades avanzadas como la sincronización con el calendario de Google. La aplicación permite a los usuarios realizar, editar y gestionar reservas con una interfaz amigable y funcional.

## Distinctividad and Complexity

### Distinctividad

Este proyecto es distintivo en varios aspectos:
- **Integración con Google Calendar**: La aplicación sincroniza las reservas con Google Calendar, proporcionando una integración que permite a los usuarios gestionar sus citas directamente desde su calendario.
- **Interfaz Dinámica y Reactiva**: Utiliza JavaScript para actualizar dinámicamente los horarios disponibles según el profesional seleccionado, mejorando la experiencia del usuario.
- **Gestión Completa de Reservas**: La aplicación no solo permite crear reservas, sino también modificarlas y eliminarlas, con una lógica robusta para garantizar que los horarios se gestionen de manera eficiente.

### Complejidad

El proyecto cumple con los requisitos de complejidad:
- **Uso Avanzado de Django**: Implementa varios modelos interrelacionados (Profesional, Paciente, HorarioAtencion, Reserva), y utiliza vistas basadas en clases y funciones para manejar la lógica del backend.
- **Funcionalidades Avanzadas**: Incluye características como la validación de horarios, sincronización con Google Calendar y una interfaz de usuario reactiva con JavaScript.
- **Compatibilidad con Dispositivos Móviles**: La interfaz está diseñada para ser completamente responsive, asegurando una experiencia de usuario óptima en dispositivos móviles.

## Estructura del Proyecto

El proyecto está dividido en las siguientes aplicaciones:

- **`armois/`**: Página de inicio y registro de atenciones.
  - **`models.py`**: Define los modelos de datos.
  - **`static/armois/`**: Archivos estáticos (CSS, JavaScript, imágenes).
  - **`templates/armois/`**: Plantillas HTML.
  - **`views.py`**: Vistas para la aplicación Armois.

- **`dashboard/`**: Gestión de usuarios, login y registro con perfiles con privilegios separados.
  - **`models.py`**: Define los modelos de datos.
  - **`static/dashboard/`**: Archivos estáticos (CSS, JavaScript).
  - **`templates/dashboard/`**: Plantillas HTML.
  - **`views.py`**: Vistas para la aplicación Dashboard.

- **`googlecalendar/`**: Módulo para la integración con Google Calendar.
  - **`google_calendar_class.py`**: Contiene la lógica para la integración con Google Calendar.
  - **`credentials.json`**: Credenciales de la API de Google Calendar (IMPORTANTE: Este archivo debe estar correctamente configurado para la sincronización).
  - **`token.json`**: Token de autenticación de Google Calendar (IMPORTANTE: Este archivo debe ser generado y configurado para la autenticación).

- **`project/`**: Configuración general del proyecto.
  - **`settings.py`**: Configuración del proyecto Django.
  - **`urls.py`**: Configuración de URL del proyecto.
  - **`wsgi.py`**: Configuración de WSGI para el proyecto.

- **`db.sqlite3`**: Base de datos SQLite para el proyecto.
- **`manage.py`**: Script para gestionar el proyecto Django.
- **`requirements.txt`**: Lista de dependencias necesarias para ejecutar el proyecto.

## Cómo Ejecutar la Aplicación

1. **Instalar Dependencias**:
   Asegúrate de tener un entorno virtual activado. Luego, instala las dependencias:
   ```bash
   pip install -r requirements.txt

## Cómo Ejecutar la Aplicación

1. **Instalar Dependencias**:
   Asegúrate de tener un entorno virtual activado. Luego, instala las dependencias:
   ```bash
   pip install -r requirements.txt

2. **Migrar la Base de Datos: Ejecuta las migraciones para configurar la base de datos**:

    ```bash
    python manage.py makemigrations
     ```

    ```bash
    python manage.py migrate
     ```

3. **Iniciar el Servidor de Desarrollo: Ejecuta el servidor de desarrollo**:

    ```bash
    python manage.py runserver

4. **Acceder a la Aplicación:**
    Abre tu navegador web y visita http://127.0.0.1:8000/ para acceder a la aplicación

## Información Adicional

- **Sincronización con Google Calendar**: La aplicación utiliza la API de Google Calendar para sincronizar las reservas. Asegúrate de configurar los archivos `credentials.json` y `token.json` correctamente en la carpeta `googlecalendar/`.

- **Responsive Design**: La interfaz ha sido diseñada para ser compatible con dispositivos móviles mediante el uso de CSS y media queries.

## Video de Demostración

Puedes ver una demostración del proyecto en acción en este [enlace a YouTube](https://www.youtube.com). El video muestra cómo se gestionan las reservas y cómo la aplicación interactúa con Google Calendar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para obtener más detalles.
