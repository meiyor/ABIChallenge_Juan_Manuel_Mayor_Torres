value_id_container=$(docker ps -aqf "name=bedrock-endpoint_frontend")
docker cp ./app.py $value_id_container:/app/
