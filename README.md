# Capstone Project / Centro Médico - Citas

## Descripción

Este proyecto es una aplicación web dinámica desarrollada con Django en el backend y JavaScript en el frontend. La aplicación está diseñada para gestionar reservas, con integración de funcionalidades avanzadas como la sincronización con el calendario de Google. La aplicación permite a los usuarios realizar, editar y gestionar reservas con una interfaz amigable y funcional.

## Funcionalidades

- **Navegación por el Sitio Web**: El sitio web está organizado en dos aplicaciones principales, `armois` y `dashboard`, cada una con su propia funcionalidad y vistas.
  
- **Registro de Horas**: Los usuarios pueden registrar horas de atención y reservas en la aplicación.

- **Selección Dinámica**: JavaScript actualiza dinámicamente las opciones disponibles en la interfaz según el profesional seleccionado.

- **Almacenamiento en Base de Datos**: Toda la información relacionada con reservas, profesionales y horarios se almacena en una base de datos SQLite.

- **Sincronización con Google Calendar**: Las reservas se sincronizan con Google Calendar para una gestión más eficiente.

### Funcionalidades en la Aplicación Dashboard

- **Login y Registro**: Gestión de usuarios con perfiles y privilegios separados.
  
- **Listado de Horarios**: Visualización de horarios y mensajes condicionales si no hay horarios disponibles.
  
- **CRUD de Reservas**: Crear, leer, actualizar y eliminar reservas con un modal.
  
- **Agregar Especialidades y Subespecialidades**: Permite agregar nuevas especialidades y subespecialidades mediante el renderizado de sólo 1 página utilizando componentes de javascript.
  
- **Agregar Profesionales**: Adición de nuevos profesionales y asignación de horarios.
  
- **Listado de Horarios Históricos**: Visualización de los horarios históricos registrados.
  
- **Logout**: Opción para cerrar sesión de manera segura.

### Funcionalidades en la Aplicación Armois

- **Página de Inicio**: Página principal con información de bienvenida y enlaces a otras secciones.
  
- **Registro de Atenciones**: Permite registrar y gestionar la información de atenciones.
  
- **Interfaz de Usuario**: Incluye estilos y scripts para mejorar la experiencia del usuario.


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
