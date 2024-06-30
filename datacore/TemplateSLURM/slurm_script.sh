#!/bin/bash
#SBATCH --job-name={{ codigo_solicitud }}
#SBATCH --output=test_job_output.txt
#SBATCH --error=test_job_error.txt
#SBATCH --partition={{ resource_type }}

echo "ESTO ES UNA PRUEBA"
# Enviar inicio de ejecución al API
response=$(curl -o /dev/null -s -w "%{http_code}\n" -X POST -H "Content-Type: application/json" -d '{"status": "started"}' http://100.27.105.231:8001/datacore/api/v1/InicioProcesamientoSolicitud/{{ codigo_solicitud }}/)

# Verificar el código de respuesta del primer curl
if [ "$response" -eq 200 ]; then
  echo "Inicio de procesamiento notificado exitosamente. Código de respuesta: $response"
else
  echo "Error al notificar el inicio de procesamiento. Código de respuesta: $response"
  exit 1
fi


# Verificar si user.sh existe y tiene permisos de ejecución
if [ -f "user.sh" ]; then
  sudo chmod +x user.sh
  ./user.sh
else
  echo "El archivo user.sh no existe."
  exit 1
fi

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
