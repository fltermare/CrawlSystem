# Web Crawler

## Usage
Start System
```bash
$ docker-compose up --scale celery_worker=4
```

Start Crawler (Simulated)
```cmd
$ docker exec -it crawlersystem_producer_1 bash


/app # python crawler.py [number of urls]
# e.g.
/app # python crawler.py 10000
```
