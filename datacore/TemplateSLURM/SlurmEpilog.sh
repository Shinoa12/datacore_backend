#!/bin/bash
# Llamar al método finish_process
curl -X POST http://tu_django_server/api/solicitudes/$SLURM_JOB_ID/finish_process/
