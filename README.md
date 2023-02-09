The application can be deployed using docker.

It contains five container services:
1. Nginx frontend routing to django framework on point 2.
2. Django Restframework 3.2 version with gunicorn server.
3. Postgres database.
4. Elasticsearch server.
5. Adminer UI to interact with postgres database.

To start the MessageCast Application, cd into the cloned directory and then run below command:
`docker-compose up`
If using Mac M1/M2 system, run below command:
`DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose up`

The application can then be accessed at `http://localhost:8080`

Once the application has started, on another terminal tab, execute below commands to run a few setup steps in the django container:
1. `docker exec -it web bash`
2. Rebuild elasticsearch index: `python3.9 manage.py search_index --rebuild`
3. Create a super admin user - `python3.9 manage.py createsuperuser`
-   fill out the prompts to create an admin user    
