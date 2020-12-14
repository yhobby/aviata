# Aviata task
## To run the application follow these steps
1. Clone repo to your local laptop or PC
2. Run the command in root folder of repo `sudo docker-compose up --build`
3. Wait until will be ready all services and midnight update will run (execute every 5 minutes) to fill the database 
4. Go to web server http://0.0.0.0:8000/

## Notes
All the libraries & tools were used for the first time (Sanic, sanic-jinja2, redis, aioredis, Celery).

All services were launched by analogy with microservice architecture in docker containers (3 container [**_web, db, worker_**]).

- **Sanic** - web server
- **sanic-jinja2** - for render data to html page
- **Celery** - to run scheduled tasks and periodic tasks
- DB - **redis** to interact with Celery & **aioredis** to interact with Sanic