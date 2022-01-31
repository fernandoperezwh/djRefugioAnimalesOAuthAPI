# djRefugioAnimalesAPIOAuth
Repositorio de prueba que implementa una API REST utilizando autentificacion por OAuth.

Esta API es consumida por un segundo proyecto de Django llamada [djRefugioAnimalesClient](https://github.com/fernandoperezwh/djRefugioAnimalesClient)


# Instalación
- Crear un entorno virtual con: ```mkvirtualenv <env_name>```
- Activar el entorno con:
    - Opción 1 -  ```workon <env_name>```
    - Opción 2  - ```source ./<env_path>/bin/activate```
- Instalar las dependencias con: ```pip install -r requirements.txt```

# Uso
- Realizar las migraciones con: ```python manage.py migrate```
- Crear super user con: ```python manage.py createsuperuser```
- Ejecutar la aplicación con: ```python manage.py runserver```

# Changelog
 - v0.3.0 Se renueva el tipo de autentirficacion habilitado el uso del protocolo OAuth
 - v0.2.1 Se elimina codigo innecesario en los ModelSerializer de Vacuna y Persona
 - v0.2.0 Integracion de Django REST Framework, se libera la api de djRefugioAnimales
 - v0.1.0 Curso de Capacitación para aprender Django