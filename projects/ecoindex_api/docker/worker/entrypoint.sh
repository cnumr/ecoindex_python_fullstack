#!/bin/sh

celery -A ecoindex.worker.tasks worker -P threads