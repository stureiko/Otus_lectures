#!/bin/bash
source env.sh

# Создание бакета
log "Creating bucket $YC_BUCKET..."
yc storage bucket create $YC_BUCKET --async
