# Paquetes para Zibanu para Django


## Paquete de autenticación y autorización de Zibanu para Django - zibanu.django.auth package

Este paquete contiene los servicios y librerias necesarias para la autenticación y autorización de usuarios a través de la API de Django. Estos componentes proporcionan la funcionalidad necesaria para gestionar la autenticación de usuarios y permitir el acceso a recursos protegidos.

El repositorio ofrece once (11) servicios API REST para el login, cambio de contraseña, listado de grupo, inicio de sesión, permisos de listado, actualización de perfil, actualización de autenticación, solicitud de contraseña, agregar usuario, eliminar usuario, listar usuarios o actualizar usuarios.   

## Paquete de Utilidades de Zibanu para Django - zibanu.django.utils package

Este paquete contiene clases de utilidad y funciones para Zibanu Django.

Estas son algunas de las clases de utilidades y funciones en este paquete:

* **zibanu.django.utils.code_generator module**:
 Esta clase se utiliza para generar diferentes tipos de códigos de forma aleatoria.
* **zibanu.django.utils.error_messages module**: Esta clase contiene constantes de compilación de mensajes de error.
* **zibanu.django.utils.mail module**: Esta clase se hereda de la clase EmailMultiAlternatives para crear un correo electrónico a partir de una plantilla html y texto html.
* **zibanu.django.utils.date_time module**: Esta clase contiene funciones para cambiar la zona horaria y agregar la zona horaria a un valor de fecha y hora.

## Paquete de Repositorio de Zibanu para Django - zibanu.django.repository package

Este sistema permite gestionar un repositorio de archivos y generar PDFs a partir de templates HTML, almacenándolos dentro del proyecto de Django y registrando la información sobre cada PDF en la tabla del repositorio, teniendo en cuenta que, se asigna una clave UUID (Universally Unique Identifier) a cada PDF generado con el fin de identificar el archivo en el repositorio.

## Paquete de Acceso de Zibanu para Django - zibanu.django.logging package

Utilidad para poder realizar el proceso de iniciar sesión (login) a través de la API.

Además, contiene señales en la API para registrar eventos importantes relacionados con el login y otros eventos de interés.

Por ejemplo, cuando un usuario realiza un inicio de sesión éxitoso, se genera una señal que activa una función para registrar la información ingresada, como el usuario que inició sesión, la hora del inicio de sesión y otros detalles relevantes, en una tabla de registro o log.
La información registrada puede incluir detalles como el tipo de acción (inicio de sesión), el usuario involucrado, la dirección IP desde la que se realizó el inicio de sesión, la fecha y hora del evento, entre otros.

Antes de registrar la información en el log, se valida si **zibanu.django.logging** está instalado en la API,
de no estarlo, se omite el registro de eventos en el log, dado que esta funcionalidad depende de su disponibilidad.

Por último, se ha creado una tabla en la base de datos para almacenar la información de registro de eventos.
Esta tabla puede tener campos como "usuario", "hora", "acción", "dirección IP", etc., para almacenar los detalles relevantes de cada evento registrado.