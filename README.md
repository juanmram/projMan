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

### Ejecución

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
5. Para conectarnos con la base de datos debemos colocar en nuestro ambiente una variable llamada **DATABASE_URL**. *Para la conexión con la base de datos actual de la aplicación contactar al desarrollador para que le provea los datos de acceso a esta*.

   ```
   # export DATABASE_URL='mysql://user:pass@server_hostname/db_name'
   ```
6. Si vamos a usar una **nueva base de datos local o remota** debemos ejecutar los siguientes comandos para migrar nuestros modelos a esta.

   ```
   # chmod +x db.py
   # python db.py db init
   # python db.py db migrate
   # python db.py db upgrade
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
   # docker build -t projman .
   # docker run -id -p 5000:5000 --name projMan --link db:mysql projman
   ```
Los pasos anteriores solo son necesarios la primera vez; cuando se desea iniciar el contenedor de nuevo solo ejecutamos:

   ```
   # docker start db projMan
   ```

## Escalabilidad

Para este caso particular se estan usando 4 maquinas virtuales, dos de ellas son usadas como servidores de aplicación y las otras dos como servidores de bases de datos. Con la siguiente distribución:

* DBServer1: 10.131.137.152
* DBServer2: 10.131.137.171
* AppServer1: 10.131.137.172
* AppServer2: 10.131.137.173

### Alta disponibilidad


**_Nota:_** En la explicación se asume que la persona que esta trabajando en este sabe sobre Linux y sus diferente herramientas como el firewall y selinux.

#### Prerequisitos
* Instalar HAProxy en los servidores de aplicación, en este caso se trabaja con la versión 1.5.18.
* Instalar MariaDB en los servidores de bases de datos, se trabajará con la versión 10.2.4.

#### Arquitectura
El sistema cuenta con dos bases de datos en replica configuradas en arquitectura "Master-Master" es decir se puede ingresar datos en cualquira de las bases de datos y esta será replicada inmediatamente a la otra base de datos. Además, se realizará el balanceo con las dos bases de datos utilizando HAProxy en los servidores de aplicación.

#### Proceso
1. Primero se configura una arquitectura "Master-Slave", donde el master es DBServer1.

   1.1 Configuraciones en DBServer1.

      1.1.1 Editar el archivo /etc/my.cnf con las siguientes lineas:

         ```
         [mysqld]
         server-id=1
         log-bin=mysql-bin
         wait_timeout=28800
         interactive_timeout=28800
         max_allowed_packet=500M

         ```

      1.1.2 Reiniciar mariadb:
         ```
         # systemctl restart mariadb
         ```
      1.1.3 Crear un usuario en la base de datos que realizará el trabajo de "Slave":

   ```
   MariaDB [(none)]> GRANT REPLICATION SLAVE ON *.* TO 'slave'@'%' IDENTIFIED BY 'projman';
   MariaDB [(none)]> FLUSH PRIVILEGES;
   MariaDB [(none)]> FLUSH TABLES WITH READ LOCK;
   ```

      1.1.4 Mostrar el estado del "Master" y copiar la información allí dada ya que serán importantes para su posterior uso. El resultado de este debe arrojar una tabla similar a la siguiente:

         ```
         MariaDB [(none)]> SHOW MASTER STATUS;
         + — — — — — — — — — + — — — — — + — — — — — — — + — — — — — — — — — +
         | File              | Position  | Binlog_Do_DB | Binlog_Ignore_DB   |
         + — — — — — — — — — + — — — — — + — — — — — — — + — — — — — — — — — +
         | mysql-bin.000001  | 639       |               |                   |
         + — — — — — — — — — + — — — — — + — — — — — — — + — — — — — — — — — +
         ```

      1.1.5 Obtener la base de datos y copiarla a DBServer2:

         ```
         # mysqldump -u root -p --database mysql > mysql.sql
         # scp mysql.sql user1@DBServer2:~/
         ```

      1.1.6 Como paso final despues de ambas configuraciones tanto en DBServer1 como en DBServer2 se deben desbloquear las tablas:

         ```
         MariaDB [(none)]> UNLOCK TABLE;
         ```

   1.2 Configuraciones en DBServer2

      1.2.1 Editar el archivo /etc/my.cnf con las siguientes lineas:

         ```
         [mysqld]
         server-id=2
         ```

      1.2.2 Reiniciar mariadb:

         ```
         # systemctl restart mariadb
         ```
      1.2.3 Importar la base de datos enviada desde DBServer1 (mysql.sql):

         ```
         # mysql -u root -p --database mysql < mysql.sql 
         ```

      1.2.4 Iniciar DBServer como "Slave" con la siguiente configuración(Donde se puede observar que "MASTER_LOG_FILE"y "MASTER_LOG_POS" son los valores arrojados anteriormente por DBServer1):

         ```
         MariaDB [(none)]> CHANGE MASTER TO MASTER_HOST='DBServer1', MASTER_USER='slave', MASTER_PASSWORD='projman', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=639;
         MariaDB [(none)]> START SLAVE;
         ```

2. Configurar la arquitectura "Master-Master".

   2.1 Configuraciones en DBServer2.

      2.1.1 Ahora es necesario editar de nuevo el archivo /etc/my.cnf con los siguientes parametros:

         ```
         [mysqld]
         server-id=2
         log-bin=mysql-bin
         wait_timeout=28800
         interactive_timeout=28800
         max_allowed_packet=500M
         ```

      2.1.2 Reiniciar mariadb:

         ```
         # systemctl restart mariadb
         ```

      2.1.3 Ingresar a MariaDB y mostrar el estado actual, al igual que en el caso anterior también será necesario utilizar las variables allí listadas:

         ```
         MariaDB [(none)]> SHOW MASTER STATUS;
         + — — — — — — — — — + — — — — — + — — — — — — — + — — — — — — — — — +
         | File              | Position  | Binlog_Do_DB | Binlog_Ignore_DB   |
         + — — — — — — — — — + — — — — — + — — — — — — — + — — — — — — — — — +
         | mysql-bin.000001  | 328       |               |                   |
         + — — — — — — — — — + — — — — — + — — — — — — — + — — — — — — — — — +
         ```

   2.2 Configuraciones en DBServer1, en este caso solo es ingresar a MariaDB y ejecutar las siguientes configuraciones con los respectivos datos:

      ```
      MariaDB [(none)]> CHANGE MASTER TO MASTER_HOST='DBServer2', MASTER_USER='slave', MASTER_PASSWORD='projman', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=328;
      MariaDB [(none)]> START SLAVE;
      ```
3. Configuraciones de balanceo de carga con arquitectura "Master-Master".

   3.1 Configuraciones en los servidores de bases de datos. Se deben crear usuarios para HAProxy, en la configuración real se necesitan crear cuatro, dos por cada maquina, sin embargo por efectos del ejemplo solo se crearan dos para que sea más sencillo con un solo servidor de aplicación (AppServer1):

         ```
         MariaDB [(none)]> CREATE USER 'haproxy_check1'@'AppServer1';
         MariaDB [(none)]> FLUSH PRIVILEGES;
         MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'haproxy_root1'@'AppServer1' IDENTIFIED BY 'projman' WITH GRANT OPTION;
         MariaDB [(none)]> FLUSH PRIVILEGES;
         ```

   3.2 Configuración de HAProxy en AppServer1.

      3.2.1 Editar el archivo /etc/haproxy/haproxy.cfg con la siguiente información:
         
         ```
         global
             log 127.0.0.1 local0 notice
             user haproxy
             group haproxy

         defaults
             log global
             retries 3
             timeout connect 5000
             timeout server 50000
             timeout client 50000

         listen mysql-cluster
             bind 10.131.137.172:3306                  # Dirección IP y puerto por el que se puede hacer el balanceo.
             mode tcp                                  # Mysql no tiene un "modo" especifico así que se utiliza TCP.
             option mysql-check user haproxy_check1    # El usuario creado para verificar el estado de Mysql
             balance roundrobin                        # Algoritmo a utilizar
             server mysql-1 10.131.137.152:3306 check  # Los servidores a los que se va a balancear
             server mysql-2 10.131.137.171:3306 check

         listen hapstats                               # (Opcional) Para ver stadisticas de los servidores
             bind 10.131.137.172:8080
             mode http
             stats enable
             stats uri /stats
         ```
      3.2.3 Se recomienda deshabilitar SELinux para que no genere problemas, por tal se en el archivo /etc/selinux/config el parametro de SELINUX debe quedar de la siguiente manera.

         ```
         SELINUX=disabled
         ```

      3.2.4 Reiniciar el servicio de HAProxy.

         ```
         # systemctl start haproxy
         ```

4. Realizar pruebas. Desde AppServer1 ejecutar consecutivamente el siguiente comando:

   ```
   # mysql -h 10.131.137.172 -u haproxy_root1 -p -e "show variables like 'server_id'"
   ```

   El cual debe arrojar las siguientes salidas(Suponiendo que el comando se lanzó 4 veces):
   ```
   +---------------+-------+
   | Variable_name | Value |
   +---------------+-------+
   | server_id     | 2     |
   +---------------+-------+

   +---------------+-------+
   | Variable_name | Value |
   +---------------+-------+
   | server_id     | 1     |
   +---------------+-------+

   +---------------+-------+
   | Variable_name | Value |
   +---------------+-------+
   | server_id     | 2     |
   +---------------+-------+

   +---------------+-------+
   | Variable_name | Value |
   +---------------+-------+
   | server_id     | 1     |
   +---------------+-------+
   ```
