import multiprocessing
import os


bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get("WEB_CONCURRENCY", "1"))
threads = int(os.environ.get("GUNICORN_THREADS", "2"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

# Allow opting into more workers without duplicating TensorFlow memory by default.
max_workers = multiprocessing.cpu_count() * 2 + 1
workers = max(1, min(workers, max_workers))
