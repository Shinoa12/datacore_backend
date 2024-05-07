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

## Migrar la base de datos

```shell
python manage.py migrate
```

## Iniciar el servidor

```shell
python manage.py runserver
```
