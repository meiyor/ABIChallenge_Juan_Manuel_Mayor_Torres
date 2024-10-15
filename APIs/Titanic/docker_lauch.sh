docker-compose -f "docker-compose.yml" up -d --build
(docker-compose up; cp -r ./mount/results/ ./results/; cp -r  ./mount/postgres/ /var/lib/postgresql/16/main/)

# use this if you want to run it directly from the Dockerfile
# docker run -t --name titanic-api-2x titanic_frontend

