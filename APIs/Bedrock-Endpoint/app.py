# import Flask dependencies

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# import the SQLAlchemy and database support modules
from models_database import db, Item

# import pytorch objects
import torch

# import this for the bedrock endpoint
import boto3
import json
import os
import random
import base64
import datetime
import string
import shutil

# read the models obtained by the ResNet18 on AWS SageMaker
checkpoint_base = torch.load("./models/model_checkpoint")
model_base = checkpoint_base["model"]
model_base.load_state_dict(checkpoint_base["state_dict"])

checkpoint_pruning = torch.load(
    "./models/model_checkpoint_Trial-2024-10-06-063816461703-ixds2")
model_pruning = checkpoint_pruning["model"]
model_pruning.load_state_dict(checkpoint_pruning["state_dict"])
# use this provisionally if you really need it or not!!

# set the boto3 values for querying
bedrock_runtime = boto3.client(
    'bedrock-runtime',
    region_name='us-west-2',
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))

# define the app object
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:DataBase@localhost:5432/apidb"
# use this configuration for docker
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:DataBase@backend_chatbot:5432/apidb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)


@app.get("/")
def index_get():
    return render_template("index.html")


@app.post("/adduser")
def adduser():
    # validate the input
    ack = 'none'
    global username
    global password
    userpass = request.get_json()
    print(userpass)
    username = userpass.get("user")
    password = userpass.get("pass")
    if len(username) == 0 or len(password) == 0:
        return (jsonify('incomplete'))
    else:
        return jsonify(ack)


@app.post("/ini")
def ini():
    global img
    global img_base64
    global interactions
    global data_cumm
    global img_cumm

    img = []
    img_base64 = ""
    interactions = 1
    data_cumm = []
    img_cumm = []
    message = {
        "answer": "Let's start having an interaction with the chatbot.. <br>"}
    return jsonify(message)


@app.post("/predict")
def predict(item=Item, db=db):
    global img
    global img_base64
    global interactions
    global data_cumm
    global username
    global img_cumm

    # This is the input of the chatbox
    text = request.get_json().get("message")

    val_temp = random.random()

    if img_base64:
        kwargs = {
              "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
              "contentType": "application/json",
              "accept": "application/json",
              "body": json.dumps({
              "anthropic_version": "bedrock-2023-05-31",
              "max_tokens": 100,
              "messages": [
                  {
                  "role": "user",
                  "content": [
                   {
                      "type": "image",
                      "source": {
                              "type": "base64",
                              "media_type": "image/jpeg",
                              "data": img_base64
                       }
                   },
                   {
                      "type": "text",
                      "text": " " + text + " \n"
                 }
               ]
              }
            ]
          })
        }

        img = []
        img_base64 = ""

    else:
        kwargs = {
              "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
              "contentType": "application/json",
              "accept": "application/json",
              "body": json.dumps({
              "anthropic_version": "bedrock-2023-05-31",
              "max_tokens": 100,
              "messages": [
                  {
                  "role": "user",
                  "content": [
                    {
                     "type": "text",
                     "text": " " + text + " \n"
                    }
                 ]
              }
            ]
          })
        }

    # get the endpoint response
    response = bedrock_runtime.invoke_model(**kwargs)

    response_text = json.loads(response['body'].read())

    # takes the input text

    print(response_text['content'][0], 'dataresponse')

    # get the time just after the query is done
    time_now = datetime.datetime.now().strftime("%I:%M:%S%p-%B-%d-%Y")

    data_cumm.append(username + ': ' + text + '\n ' + ' ChatBot: ' + \
                     response_text['content'][0]['text'] + '\n ' + time_now + '\n ')

    message = {"answer": response_text['content'][0]['text']}

    # save in the database after 5 interactions
    if interactions % 5 == 0:

        # random 16-char  code generator for each successful prediction and
        # ID generator
        code_str = ''.join(random.choice(string.ascii_letters)
                           for i in range(16))
        id = random.randint(0, 5000)

        file_ids_r = open("./ids.txt", "r")
        lst = []
        for line in file_ids_r:
            lst.append(int(line.strip()))

        # check if the ids are repeated
        while id in lst:
            id = random.randint(0, 5000)

        # create file with new ids to save in the database
        with open("./ids.txt", "a+") as file_ids:
            file_ids.write(str(id) + '\n')

        time_after = datetime.datetime.now().strftime("%I:%M:%S%p-%B-%d-%Y")

        # fill the database item values
        register = item(
            id=id,
            code=code_str,
            date=time_after,
            username=username,
            Interaction_Register=data_cumm,
            Images_Files=img_cumm)
        data_cumm = []
        img_cumm = []

        # add a new register to the database
        db.session.add(register)
        db.session.commit()

        # generate the database_copy folder
        if not os.path.exists('./database_copy/'):
            os.makedirs('./database_copy/', exist_ok=True)

        # copy the files from a database to the other
        if os.path.exists('/var/lib/postgresql/15/main/'):
            shutil.copytree(
                '/var/lib/postgresql/15/main/',
                './database_copy/',
                dirs_exist_ok=True)

    interactions = interactions + 1

    return jsonify(message)


@app.post("/img_capture")
def img_capture():
    global img
    global img_base64
    global img_cumm

    # This is the img input of the chatbox
    results_img = request.get_json().get("results_img")

    file_name = request.get_json().get("file_name")

    img = base64.b64decode(results_img.split(',')[1])
    img_base64 = results_img.split(',')[1]

    # generate image list when the image query is requested
    img_cumm.append(file_name + ': ' + img_base64 + '; ')

    print(file_name + ': ' + img_base64 + '; ')
    message = {"answer": "loading img!"}
    return jsonify(message)


if __name__ == "__main__":
    # create the table in the database
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # run the main in localhost
    # app.run(port=5000, debug=True)
    # run this for Docker
    app.run(host='0.0.0.0', port=8000, debug=True)
