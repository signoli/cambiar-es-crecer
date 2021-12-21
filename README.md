# CAMBIAR ES CRECER

## PREREQUISITOS
### Mac/Linux
* Acceso a la `shell` del SO o mas conocido como `terminal`

### Windows
* Tener [python](https://www.python.org/downloads/) instalado en el sistema (Mac/Linux ya tienen instalado python 2.7 por defecto)
* [git bash](https://github.com/git-for-windows/git/releases/download/v2.34.1.windows.1/Git-2.34.1-64-bit.exe) (para usuarios de Windows)


## INSTALACION

1. Crear un entorno con virtualenv
   ```zsh
   $ pip install virtualenv
   $ virtualenv -p python3 ~/cec-entorno
   $ cd ~/cec-entorno 
   ## En Linux/Mac
   $ source bin/activate
   ## En Windows
   $ source Scripts/activate 
   ```
2. Clonar este repositorio
    ```zsh
    $ cd ~/
    $ git clone https://github.com/signoli/cambiar-es-crecer.git
    ```
3. Instalar las dependencias del proyecto
   ```zsh
    $ cd ~/cambiar-es-crecer
    $ pip install -r requirements.txt
    ```
4. Correr la aplicacion
    ```zsh
    $ python manage.py runserver
    ```

## CORRER MIGRATIONS

Si cambia un modelo, como puede ser el modelo de la entidad Post, es necesario crear las migrations necesarias para que base de datos este actualizada y sea funcional. Para ello se debe realizar lo siguiente:

1. Agregar los cambios correspondientes a cualquiera de los modelos. Ejemplo: /blog/posts/models.py.
2. Correr las migrations de la aplicacion o package que se modifico.
   ```zsh
   $ python manage.py makemigrations blog
   ```
3. Correr las migrations
   ```zsh
   $ python manage.py migrate
   ```