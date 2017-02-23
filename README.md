# ProjMan#

## Descripción
ProjMan es una aplicación web pensada para organizar los proyectos de una empresa donde lo que se busca es poder asociar a los diferentes empleados un rol característico en un departamento de la compañía o proyecto, con la finalidad de llevar registro de los responsables en cada labor.

La aplicación fue desarrollada con el uso del microframework **Flask** basado en python. El proyecto ha sido desplegado en **Docker** y **Heroku**.

## Instalación
### Prerrequisitos
* Python 2.7
* Pip (Python)
* MariaDB >= v10 (Despliegue Local)

### Estructura
   ```
   .
   ├── app
   │   ├── __init__.py
   │   ├── models.py
   │   ├── static
   │   │   ├── css
   │   │   │   ├── app.css
   │   │   │   ├── foundation.css
   │   │   │   └── foundation.min.css
   │   │   ├── index.html
   │   │   ├── js
   │   │   │   ├── app.js
   │   │   │   └── vendor
   │   │   │       ├── foundation.js
   │   │   │       ├── foundation.min.js
   │   │   │       ├── jquery.js
   │   │   │       └── what-input.js
   │   │   └── requirements.txt
   │   ├── templates
   │   │   ├── create.html
   │   │   ├── edit.html
   │   │   └── index.html
   │   └── views.py
   ├── db.py
   ├── Dockerfile
   ├── env
   ├── instance
   │   └── config.py
   ├── Procfile
   ├── README.md
   ├── requirements.txt
   └── run.py
   ```
###Ejecución
Para la correcta ejecución de la aplicación debemos asegurarnos de estar usando la última versión de Python 2, debido a que con versiones 3.x comienzan a presentarse problemas de compatibilidad. Debemos seguir los siguientes pasos para lograr su correcto funcionamiento:

1. Descargar el repo, mediante el comando.

   ```
   # git clone https://github.com/jyepesr1/projMan
   ```
2. Se debe configurar la base de datos en caso tal que el despliegue se vaya a realizar de manera local. La aplicación esta desarrollada bajo MySQL, por lo tanto solo de debe crear un usuario con una contraseña en MariaDB que tenga permisos sobre nuestra base de datos.

3. Vamos a instalar *virtualenv* que nos permitirá manejar ambientes de desarrollo locales para no afectar nuestro ambiente normal y nos facilitará el manejo de versiones de paquetes entre aplicaciones, con la finalidad de evitar conflictos. Para eso usaremos los siguientes comandos:

   ```
   # mkdir projMan/env
   # pip install virtualenv
   # virtualenv projMan/env
   # source projMan/env/bin/activate
   ```
Nuestro ambiente virtual ahora se encuentra configurado en la carpeta *env/*

4. Ahora para poder instalar todas las dependencias necesarias para que nuestro programa ejecute, usaremos de nuevo el comando *pip* con el archivo de requisitos de la aplicación.

   ```
   # pip install -r requirements.txt
   ```
5. Si vamos a usar una **nueva base de datos local o remota** debemos ejecutar los siguientes para migrar nuestros modelos a esta.

   ```
   # chmod +x db.py
   # python db.py init
   # python db.py migrate
   # python db.py upgrade
   ```
6. Para conectarnos con la base de datos debemos colocar en nuestro ambiente una variable llamada **DATABASE_URL**. *Para la conexión con la base de datos actual de la aplicación favor contactar al desarrollador para que este le provea los datos de acceso orginales*.

   ```
   # export DATABASE_URL='mysql://user:pass@server_hostname/db_name'
   ```
7. Ahora solo falta iniciar el servidor, el cual por defecto corre en el puerto 5000.

   ```
   # python run.py
   ```
Podemos acceder a la aplicación entrando a http://localhost:5000

## Despliegue
### Heroku
La aplicación ha sido desplegada bajo la url http://projman.herokuapp.com/

### Docker
La aplicación también ha sido desplegada en docker nativo (Linux) mediante el uso del Dockerfile y los siguientes comandos:

   ```
   # docker run --name db -e MYSQL_ROOT_PASSWORD=test -d -p 3306:3306 mariadb
   # docker build -t projMan .
   # docker run -id -p 5000:5000 --name projMan --link db:mysql projman
   ```
Los pasos anteriores solo son necesarios la primera vez; cuando se desea iniciar el contenedor de nuevo solo ejecutamos:

   ```
   # docker start db projMan
   ```

