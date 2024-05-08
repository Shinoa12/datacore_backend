# DataCore — Backend

Sigue los pasos siguientes para configurar tu entorno e iniciar el servidor.

## Crear el entorno virtual

```shell
python -m venv .venv
```

## Activar el entorno virtual

### Windows

#### CMD

```shell
.venv\Scripts\activate.bat
```

#### PowerShell

```shell
.\.venv\Scripts\activate.ps1
```

### macOS/Linux

```shell
source .venv/bin/activate
```

## Instalar las dependencias necesarias

```shell
pip install -r requirements.txt
```

## Configurar las variables de entorno

Crea un archivo con el nombre `.env` en la raíz del directorio del proyecto y agrega las variables de entorno siguientes con los **valores específicos** que correspondan a tu entorno de desarrollo.

```shell
SECRET_KEY=CLAVE_SECRETA
DB_HOST=TU_HOST
DB_PORT=TU_PUERTO
DB_USER=TU_USUARIO
DB_PASS=TU_CONTRASEÑA
DB_NAME=TU_NOMBRE
```

## Migrar la base de datos

```shell
python manage.py migrate
```

## Iniciar el servidor

```shell
python manage.py runserver
```
