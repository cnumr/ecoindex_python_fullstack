#!/bin/sh

celery -A ecoindex.worker.tasks worker --queues=ecoindex,ecoindex_batch