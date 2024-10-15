docker-compose up;
docker run --network="host" bedrock-endpoint_frontend_chatbot

# uncomment this if necessary...
# cp -r /var/lib/postgresql/16/main/* ./mounts/postgres/
# docker-compose -f "docker-compose.yml" up -d --build

#cp -r ./mounts/postgres/ /var/lib/postgresql/16/main/)

# use this if you want to run it directly from the Dockerfile
# docker run -t --name titanic-api-2x titanic_frontend

