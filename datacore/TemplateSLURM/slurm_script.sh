#!/bin/bash
#SBATCH --job-name={{ codigo_solicitud }}
#SBATCH --output=test_job_output.txt
#SBATCH --error=test_job_error.txt
#SBATCH --partition={{ resource_type }}


# Enviar inicio de ejecución al API
curl -X POST -H "Content-Type: application/json" -d '{"status": "started"}' http://100.27.105.231:8001/datacore/api/v1/InicioProcesamientoSolicitud/{{ codigo_solicitud }}/
nombre_sh={{ user_bash }}

sudo chmod +x nombre_sh
./nombre_sh

# Verificar si existe la carpeta 'resultados'
if [ -d "resultados" ]; then
  echo "La carpeta 'resultados' si existe"
else
  echo "La carpeta 'resultados' no existe. Creándola ahora..."
  mkdir resultados
fi

mv test_job_output.txt resultados/
mv test_job_error.txt resultados/

zip -r resultados.zip resultados

# Enviar solicitud HTTP a la API para notificar el final del proceso

curl -X POST -H "Content-Type: multipart/form-data" -F "status=finished" -F "id_solicitud={{ codigo_solicitud }}" -F "file=@resultados.zip" http://100.27.105.231:8001/datacore/api/v1/FinProcesamientoSolicitud/

rm -rf resultados
rm resultados.zip
