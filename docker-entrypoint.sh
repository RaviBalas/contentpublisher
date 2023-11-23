#!/usr/bin/env bash
#python3 manage.py makemigrations
python3 manage.py migrate 
# celery
#celery -A core worker -l DEBUG --concurrency=3 -Q user_tasks > /target/user_tasks.out 2>&1 &
#celery -A core worker -l DEBUG --concurrency=3 -Q file_to_pages > /target/file_to_pages.out 2>&1 &
#celery -A core worker -l DEBUG --concurrency=3 -Q doc_classifier > /target/doc_classifier.out 2>&1 &
#celery -A core worker -l DEBUG --concurrency=3 -Q kyc_ocr > /target/kyc_ocr.out 2>&1 &
#celery -A core worker -l DEBUG --concurrency=3 -Q health_ocr > /target/health_ocr.out 2>&1 &
#celery -A core worker -l DEBUG --concurrency=3 -Q send_for_qc > /target/send_for_qc.out 2>&1 &
python3 manage.py runserver 0.0.0.0:8080
