$(document).ready(function () {
  // Manejo del form login
  form = document.getElementById('login-form');
  form.addEventListener('submit', function (event) {
    event.preventDefault() // Evita que el formulario se envíe inmediatamente

    var username = document.getElementById('usernameLogin').value
    var password = document.getElementById('passwordLogin').value

    // Validaciones básicas
    if (!username || !password) {
      alert('Por favor, complete todos los campos.')
      return
    }
    // Enviar el formulario después de mostrar el alert
    event.target.submit()
  })

  // Maneja el clic en el botón de alternancia
  $('.blmd-switch-button').on('click', function () {
    // Alterna las clases de visibilidad entre el formulario de inicio de sesión y el de registro
    $('#login-form').toggleClass('form-hidden')
    $('#Register-form').toggleClass('form-hidden')

    // Ajusta el botón de alternancia
    $(this).toggleClass('active')

    // Ajusta el contenedor de color
    $('.blmd-color-conatiner').toggleClass('ripple-effect-All')
  })

  // Opcional: Agrega un efecto de "ripple" al botón
  $('.btn-blmd').on('click', function (e) {
    var $ink = $('<span class="ink"></span>')
    var d, x, y

    $(this).append($ink)

    // Calcula el tamaño y la posición del efecto de "ripple"
    d = Math.max($(this).outerWidth(), $(this).outerHeight())
    $ink
      .css({
        width: d,
        height: d,
        left: e.pageX - $(this).offset().left - d / 2,
        top: e.pageY - $(this).offset().top - d / 2
      })
      .addClass('animate')

    // Limpia el efecto después de la animación
    $ink.one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
      $(this).remove()
    })
  })
})