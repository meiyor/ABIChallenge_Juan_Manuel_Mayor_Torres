# -*- coding: utf-8 -*-
"""
Created on Tuesday October 8 2024

@author: JMM
"""

# 1. Library imports
from fastapi import Depends, FastAPI, HTTPException, Request
from titanic import Titanic
import uvicorn
import numpy as np
import pickle
import pandas as pd
import joblib
import base64
import datetime
import random
import string
import shap
import datetime
import matplotlib.pyplot as plt

# import the SQLAlchemy and database support modules
import crud
import models_database
import schemas_database
from database import engine, get_db

# BytesIO
from io import BytesIO
from openpyxl.utils.dataframe import dataframe_to_rows
import openpyxl

# import fastapi responses
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# define the excel writer function


def df_to_excel(df, ws, header=True, index=True, startrow=0, startcol=0):

    rows = dataframe_to_rows(df, header=header, index=index)

    for r_idx, row in enumerate(rows, startrow + 1):
        for c_idx, value in enumerate(row, startcol + 1):
            ws.cell(row=r_idx, column=c_idx).value = value


# set the database models here
models_database.Base.metadata.create_all(bind=engine)

# 2. Create the app object and load the previous trained pkls
app = FastAPI()
templates = Jinja2Templates(directory='./templates/')

# set the folders for the static files reference in the frontend
app.mount("/static", StaticFiles(directory='static'), name="static")
app.mount("/results", StaticFiles(directory='results'), name="results")

# read the models giving by the training notebook
file_models = open("./models/models_titanic.pkl", 'rb')
models_pickle = pickle.load(file_models)
explainers_pickle = joblib.load("./models/explainers_titanic.pkl")

# set the columns the input must have
must_have_columns = [
    'Pclass',
    'Sex',
    'Age',
    'SibSp',
    'Parch',
    'Fare',
    'Embarked',
    'Title',
    'FamilySize',
    'IsAlone',
    'Age*Class']

# parse database session
session_db = Depends(get_db)

# 3. define post and get here


@app.get('/upload', response_class=HTMLResponse)
def get_form(request: Request):
    hyperlink = ""
    return templates.TemplateResponse(
        "index.html", {
            "request": request, "hyperlink": hyperlink})


@app.post('/upload', response_class=HTMLResponse)
def post_form(
        request: Request,
        form_data: Titanic = Depends(
            Titanic.as_form),
    must_have_columns=must_have_columns,
    item=schemas_database.ItemCreate,
        db=session_db):

    # open and validate the input .csv file
    try:
        contents = form_data.file.file.read()
        buffer = BytesIO(contents)
        df = pd.read_csv(buffer)
    except BaseException:
        df = []
        raise HTTPException(status_code=500,
                            detail='Something went wrong in the connection')
    finally:
        buffer.close()
        form_data.file.file.close()

    # remove the unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # validate the df life just as is given as input in the training notebook
    if len(df.columns) != 11 or len(df.columns) < 11:
        status_message = 'input is not allowed - input doesnt have the (correct) or enough amount of columns'

        with open("./static/gray.jpg", "rb") as filef:
            roc_encoded_image = base64.b64encode(filef.read()).decode("utf-8")

        print('input is not allowed - input doesnt have the (correct) or enough amount of columns')
    else:
        must_have_columns = [x.lower() for x in must_have_columns]
        columns_val = [x.lower() for x in df.columns]

        if len(df.columns) > 11:
            status_message = 'input is not allowed - input doesnt have the (correct) or enough amount of columns'

            with open("./static/gray.jpg", "rb") as filef:
                roc_encoded_image = base64.b64encode(
                    filef.read()).decode("utf-8")

            print('data has more allowed columns! please re-check your input!')
        elif len(df.columns) == 11 and must_have_columns == columns_val:

            predict_strings = []

            # succesful prediction validation here!
            # process the df to process the trained models here
            df.fillna(0, inplace=True)
            df = df.astype(int)
            X_test = df.copy()

            # check the model predictions
            predictions = models_pickle[int(
                form_data.select_model)].predict(X_test)
            proba = models_pickle[int(
                form_data.select_model)].predict_proba(X_test)
            acc_val = str(models_pickle[int(form_data.select_model) + 6])
            # create the predict string list
            for index in range(0, len(predictions)):
                if predictions[index] == 0:
                    predict_strings.append('No Survive')
                else:
                    predict_strings.append('Survive')

            # get the time just after the prediction is done
            time_now = datetime.datetime.now().strftime("%I:%M:%S%p-%B-%d-%Y")

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
                file_ids.write(str(id))

            # fill the database item values
            item.id = id
            item.date = time_now
            item.username = form_data.username
            item.code = code_str

            # model name definition
            if int(form_data.select_model) == 0:
                item.model = 'Logistic Regression'
            elif int(form_data.select_model) == 1:
                item.model = 'SVM'
            elif int(form_data.select_model) == 2:
                item.model = 'KNN-3'
            elif int(form_data.select_model) == 3:
                item.model = 'Gaussian NB'
            elif int(form_data.select_model) == 4:
                item.model = 'Random Forest'
            elif int(form_data.select_model) == 5:
                item.model = 'XGBoost'

            # fill the database item values
            item.prediction_probability = proba
            item.prediction = predict_strings
            item.explainability_file = form_data.username + '-' + \
                str(id) + '-' + code_str + '-' + item.model + '-' + time_now + '.jpg'
            item.results_file = form_data.username + '-' + \
                str(id) + '-' + code_str + '-' + item.model + '-' + time_now + '.xls'

            # save and create the explainability image
            shap_values_test = explainers_pickle[int(
                form_data.select_model)].shap_values(X_test)
            if len(shap_values_test.shape) == 3:
                shap_values_test = np.mean(shap_values_test, axis=2)
            shap.summary_plot(shap_values_test, X_test, show=False)
            plt.savefig('./results/explain/' + item.explainability_file)

            # save the results file as xls
            df_res = pd.DataFrame(
                columns=[
                    'Prediction',
                    'No Survive probability',
                    'Survive Probability'])
            df_res['Prediction'] = predict_strings
            df_res['No Survive probability'] = proba[:, 0]
            df_res['Survive Probability'] = proba[:, 1]
            # df_res['Index'] = df_res.index

            name_result_file = form_data.username + '-' + \
                str(id) + '-' + code_str + '-' + item.model + '-' + time_now + '.xls'

            # saving the xls resulting file
            wb = openpyxl.Workbook()
            df_to_excel(df_res, wb.active)
            wb.save('./results/xls/' + name_result_file)

            # add a new register to the database
            crud.create_item(db=db, item=item)

            # set the status messages
            status_message = "The select model's train accuracy is: " + acc_val + \
                '%, for ' + item.model + 'model, please refer to the result output file here: '
            hyperlink_message = name_result_file

            # reading the ROC results giving by the training
            with open("./static/ROC_training_results.jpg", "rb") as roc_file:
                roc_encoded_image = base64.b64encode(
                    roc_file.read()).decode("utf-8")

            # reading explainability plot
            with open('./results/explain/' + item.explainability_file, "rb") as explain_file:
                explain_image = base64.b64encode(
                    explain_file.read()).decode("utf-8")

        else:
            status_message = 'data does not have the right column names!'
            print('data does not have the right column names!')
            with open("./static/gray.jpg", "rb") as filef:
                roc_encoded_image = base64.b64encode(
                    filef.read()).decode("utf-8")

    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "ROCImage": roc_encoded_image,
                                       "status_message": status_message,
                                       "explain_img": explain_image,
                                       "hyperlink": hyperlink_message})


# 4. Run the API with the fastapi command
#    Will run on http://0.0.0.0:8000
if __name__ == '__main__':
    # uvicorn.run(app, host='127.0.0.1', port=8000)
    uvicorn.run(app, host='0.0.0.0', port=8000)

