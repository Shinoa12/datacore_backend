#!/bin/bash

# Enviar inicio de ejecución al API
curl -X POST -H "Content-Type: application/json" -d '{"status": "started"}' http://datacore/api/v1/InicioProcesamientoSolicitud/{{ solicitud.codigo_solicitud }}/

#!/bin/bash
#SBATCH --job-name={{ solicitud.codigo_solicitud }}
#SBATCH --output=output_%j.txt
#SBATCH --error=error_%j.txt
#SBATCH --partition={{ resource_type }}


# Script del usuario
{{ user_script }}



# Script del usuario
#{{ user_script }}

# Enviar el trabajo a SLURM y guardar el ID del trabajo
#JOB_ID=$(sbatch user_script.sh | awk '{print $4}')

# Esperar a que el trabajo termine
#while true; do
#    JOB_STATE=$(sacct -j $JOB_ID --format=State --noheader | awk '{print $1}')
#    if [[ "$JOB_STATE" == "COMPLETED" || "$JOB_STATE" == "FAILED" || "$JOB_STATE" == "CANCELLED" ]]; then
#        break
#    fi
#    sleep 10
#done

#OUTPUT_FILE=output_${JOB_ID}.txt

# Copiar el archivo de salida al controlador (dcprincipal)
#scp $OUTPUT_FILE slurm@dcprincipal:/path/to/destination/

# Enviar solicitud HTTP a la API para notificar el final del proceso
curl -X POST -H "Content-Type: application/json" -d '{"status": "finished"}' http://datacore/api/v1/FinProcesamientoSolicitud/{{ solicitud.codigo_solicitud }}/
