value_id_container=$(docker ps -aqf "name=titanic_frontend")
docker cp $value_id_container:/app/database_copy/ ./mounts/postgres/
docker cp $value_id_container:/app/ids.txt ./