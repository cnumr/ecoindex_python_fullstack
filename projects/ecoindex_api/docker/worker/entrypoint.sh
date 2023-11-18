#!/bin/sh

celery -A worker.tasks worker -P threads