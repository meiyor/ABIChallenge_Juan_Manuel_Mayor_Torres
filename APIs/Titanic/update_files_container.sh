value_id_container=$(docker ps -aqf "name=titanic_frontend")
docker cp ./app.py $value_id_container:/app/
docker cp ./database.py $value_id_container:/app/
