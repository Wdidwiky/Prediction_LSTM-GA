# Railway Deployment

## Required files

- `railway.json` sets Railpack as the builder, uses Gunicorn as the start command, and enables `/health` as the health check.
- `requirements.txt` contains production dependencies for Railway's Python build.
- `runtime.txt` requests Python 3.11.
- `gunicorn.conf.py` binds Gunicorn to Railway's `PORT` environment variable.

## Railway variables

Set these in Railway's service Variables tab:

```env
SECRET_KEY=replace-with-a-long-random-value
```

Optional variables:

```env
TICKER=BZ=F
START_DATE=2022-12-30
TIME_STEP=60
CACHE_TYPE=SimpleCache
CACHE_DEFAULT_TIMEOUT=600
WEB_CONCURRENCY=1
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=120
```

Keep `WEB_CONCURRENCY=1` unless the service has enough memory, because every worker loads the TensorFlow model.

## Deploy steps

1. Push this repository to GitHub.
2. Create a Railway project from the GitHub repository.
3. Confirm the root directory is the repository root.
4. Add `SECRET_KEY` in Variables.
5. Deploy.

The app health check is available at `/health`. The main app remains at `/`.
