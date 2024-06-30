#!/bin/bash
#SBATCH --job-name={{ codigo_solicitud }}
#SBATCH --output=test_job_output.txt
#SBATCH --error=test_job_error.txt
#SBATCH --account=slurm
#SBATCH --partition={{ resource_type }}

# Definir un directorio de trabajo
WORKDIR=/home/ubuntu/datacore/
LOGFILE="$WORKDIR/script.log"

# Crear el directorio de trabajo si no existe
mkdir -p $WORKDIR

# Moverse al directorio de trabajo
cd $WORKDIR

# Función para registrar mensajes en el archivo de log
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOGFILE
}

log "Script iniciado"

# Información del entorno
log "Usuario: $(whoami)"
log "Directorio actual: $(pwd)"
log "Archivos en el directorio: $(ls -l)"

# Notificar al API sobre el inicio del proceso
log "Inicio de copia de archivos"
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"status": "started"}' http://100.27.105.231:8001/datacore/api/v1/InicioProcesamientoSolicitud/{{codigo_solicitud}}/)

if [ $response -eq 200 ]; then
    log "Notificación de inicio enviada exitosamente"
else
    log "Error al enviar la notificación de inicio"
fi

# Cambiar permisos y ejecutar user.sh
log "Cambiando permisos y ejecutando user.sh"
chmod +x $WORKDIR/user.sh
log "Permisos cambiados, ejecutando user.sh"
./user.sh
log "user.sh ejecutado"

# Verificar si existe la carpeta 'resultados'
if [ -d "resultados" ]; then
    log "La carpeta 'resultados' sí existe"
else
    log "La carpeta 'resultados' no existe. Creándola ahora..."
    mkdir resultados
fi

# Mover archivos de salida a la carpeta 'resultados'
log "Moviendo archivos de salida a la carpeta 'resultados'"
mv test_job_output.txt resultados/
mv test_job_error.txt resultados/

# Crear un archivo zip con los resultados
log "Creando un archivo zip con los resultados"
zip -r resultados.zip resultados

# Notificar al API sobre el final del proceso
log "Enviando notificación de finalización al API"
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: multipart/form-data" -F "status=finished" -F "id_solicitud={{ codigo_solicitud }}" -F "file=@resultados.zip" http://100.27.105.231:8001/datacore/api/v1/FinProcesamientoSolicitud/)

if [ $response -eq 200 ]; then
    log "Notificación de finalización enviada exitosamente"
else
    log "Error al enviar la notificación de finalización"
fi

# Limpiar archivos temporales
log "Limpiando archivos temporales"

log "Script completado"

