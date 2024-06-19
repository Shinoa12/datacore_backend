#!/bin/bash
# Llamar al método start_process
curl -X POST http://tu_django_server/api/solicitudes/$SLURM_JOB_ID/start_process/
