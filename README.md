# Web Crawler

## Usage
Start System
```bash
$ docker-compose up --scale celery_worker=4
```

Start Crawler (Simulated)
```cmd
$ docker exec -it crawlersystem_celery_producer_1 bash


/app # python crawler.py [number of urls]
/app # python crawler.py 10000                  # e.g.
```
