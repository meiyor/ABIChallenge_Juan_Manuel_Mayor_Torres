value_id_container=$(docker ps -aqf "name=bedrock-endpoint_frontend")
docker cp $value_id_container:/app/database_copy/ ./mounts/postgres/
docker cp $value_id_container:/app/ids.txt ./
