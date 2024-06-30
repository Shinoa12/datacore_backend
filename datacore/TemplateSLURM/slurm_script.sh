#!/bin/bash
#SBATCH --job-name=100
#SBATCH --output=test_job_output.txt
#SBATCH --error=test_job_error.txt
#SBATCH --account=slurm
#SBATCH --partition=resource1

# Ruta al archivo de log
LOGFILE="script.log"

# Función para registrar mensajes en el archivo de log
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOGFILE
}

log "Script iniciado"

# Información del entorno
log "Usuario: $(whoami)"
log "Directorio actual: $(pwd)"
log "Archivos en el directorio: $(ls -l)"

# Enviar inicio de ejecución al API
log "Inicio de copia de archivos"
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d '{"status": "started"}' http://100.27.105.231:8001/datacore/api/v1/InicioProcesamientoSolicitud/100/)

# Verificar si la solicitud fue exitosa
if [ $response -eq 200 ]; then
    log "Notificación de inicio enviada exitosamente"
else
    log "Error al enviar la notificación de inicio"
fi

# Cambiar permisos y ejecutar user.sh
log "Cambiando permisos y ejecutando user.sh"
sudo chmod +x user.sh
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

# Enviar solicitud HTTP a la API para notificar el final del proceso
codigo_solicitud=100  # Reemplazar con el valor adecuado
log "Enviando notificación de finalización al API"
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: multipart/form-data" -F "status=finished" -F "id_solicitud=$codigo_solicitud" -F "file=@resultados.zip" http://100.27.105.231:8001/datacore/api/v1/FinProcesamientoSolicitud/)

# Verificar si la solicitud fue exitosa
if [ $response -eq 200 ]; then
    log "Notificación de finalización enviada exitosamente"
else
    log "Error al enviar la notificación de finalización"
fi

# Limpiar archivos temporales
log "Limpiando archivos temporales"
rm -rf resultados
rm resultados.zip

log "Script completado"
