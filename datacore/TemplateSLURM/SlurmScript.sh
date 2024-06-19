#!/bin/bash
#enviar iniciode ejecucion al api
curl -X POST -H "Content-Type: application/json" -d '{"status": "started"}' http://datacore/api/solicitudes/{{ solicitud.id }}/start_process/

# Script del usuario
{{ user_script }}

# Comandos adicionales si es necesario
sbatch user_script.sh

OUTPUT_FILE=output_${SLURM_JOB_ID}.txt

# Copiar el archivo de salida al controlador (dcprincipal)
scp $OUTPUT_FILE slurm@dcprincipal:/path/to/destination/

# Enviar solicitud HTTP a la API para notificar el final del proceso
curl -X POST -H "Content-Type: application/json" -d '{"status": "finished"}' http://datacore/api/solicitudes/{{ solicitud.id }}/finish_process/
