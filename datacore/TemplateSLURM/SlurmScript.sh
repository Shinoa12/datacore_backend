#!/bin/bash
#SBATCH --job-name={{ solicitud.codigo_solicitud }}
#SBATCH --output=output_%j.txt
#SBATCH --error=error_%j.txt
#SBATCH --partition={{ resource_type }}

# URLs de tu API Django
START_PROCESS_URL="http://datacore/api/solicitudes/{{ solicitud.id }}/start_process/"
FINISH_PROCESS_URL="http://datacore/api/solicitudes/{{ solicitud.id }}/finish_process/"

# Prolog y Epilog para srun
#SBATCH --prolog=slurm_prolog.sh
#SBATCH --epilog=slurm_epilog.sh

# Script del usuario
{{ user_script }}

# Comandos adicionales si es necesario
srun {{ solicitud.parametros_ejecucion }}


