# ABIChallenge_Juan_Manuel_Mayor_Torres
Infinita Consulting test for ML Engineer position

In This README we will describe the process for executing this API code locally and through **Docker** container. The steps outline for this execution will be:

- **Configuration**
- **Notebook Running (offline training)**
- **API local releasing**
- **API Docker**
- **SonarCloud test**

## Configuration

The first to do is to **git clone** this repository in your local machine, be sure if you install **Docker** completely on your machine. For **Ubuntu** or any related unix
distribution, follow the steps described here [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu). If you are using Windows or Mac
please refer to other OS installation types here [https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/) and here [https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/) respectively.

After you clone this repository and get the basic **Python** and **pip** **devs** on your machine, go to the **Titanic** folder and install the requirements 


```python
pip install -r requirements.txt
```
Now before evaluating the code on the notebook you will need to install **Jupyter notebook** on you machine 

from **pip**

```python
pip install notebook
```
 
 or from **apt**

```bash
 apt install python3-notebook jupyter jupyter-core python-ipykernel
 ```

After you installed and check the **Jupyter Notebook** installation, you must add the environment to your jupyer environments, just follow the following commands in sequence and restart your machine.

```bash

# activating environment
 source /location_of_the_environment/myenv/bin/activate # be sure where is your environment located after you install the requirements
 pip install ipython
 pip install ipykernel
 pip install bash_kernel

# setting the kernel
 ipython kernel install --user --name=myenv
 python -m ipykernel install --user --name=myenv

 python -m bash_kernel.install
 ```

Remember to run the previous commands after you have your environment activated and deploy **Jupyter Notebook**

```bash
jupyter notebook --allow-root # run this having your environment activated
```

You can change and set your environment clicking on the Kernel menu of jupyter here:

![image](https://github.com/user-attachments/assets/4f07f9a8-51d9-4519-8d65-8fb5ae737e3f)

Now, you can continue with the Notebook execution.

## Notebook Running (offline training)

To refer the notebook file for training offline the [Titanic Kaggle Dataset](https://www.kaggle.com/code/startupsci/titanic-data-science-solutions) you can go to the following [link](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/blob/main/APIs/Titanic/training_titanic_model.ipynb).

After you open the .ipynb file for the Titanic API you will see the following screen.

![image](https://github.com/user-attachments/assets/b9104be0-8126-4062-9e55-0714873d59f5)

Then, be sure that your environment is loaded in your Jupyter IDE, and you can start running the notebook in sequence. Take into account that this notebook **is not** exactly the same as the Kaggle repository but it has the same sequence in order to debug, remove, and include new features for the subsequent model training and saving.

Here you can see a couple of snapshots of the notebook where the features has been debugged:

![image](https://github.com/user-attachments/assets/e748c61c-c283-4e3c-8056-bc0fc7770a89)
![image](https://github.com/user-attachments/assets/474ca140-1e03-44c6-8330-94e39a7ed90e)

After you are sure you have executed all the data debugging cells (in sequence), then you focused on the dataframe preparation, training, and models/training releasing at the end of the notebook. Here you can see a snapshot of the models training cell in the notebook

![image](https://github.com/user-attachments/assets/76d25e07-9277-4e91-828c-55724872640c)

The notebook included the training and evaluation of six different models from **scikit-learn**, such as, **LogisticRegression**, **SVC/SVM**, **KNN** (with 3 nearest-neighbors), **Gaussian NB**, **RandomForest**, and **XGBoost**.
At the end of the cell you can see the lines we used for saving the **pkl** containing the [**models**](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/blob/main/APIs/Titanic/models/models_titanic.pkl) and the SHAP [**explainers**](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/blob/main/APIs/Titanic/models/explainers_titanic.pkl). To see a more deep explaination of the Shapley Value explainability for tabular data go to his [paper](https://proceedings.mlr.press/v119/sundararajan20b.html) and the [Shapley library](https://shap.readthedocs.io/en/latest/generated/shap.Explainer.html). 

![image](https://github.com/user-attachments/assets/b2e91293-f074-4706-99c0-16f3e3440c68)

You can also check the ROC curve for the training metrics. In the last part of the notebook, here you can refer to the corresponding snapshot.

![image](https://github.com/user-attachments/assets/3889afe9-5ff5-4ab6-a555-cfa104eebcfc)


In the final API functionality this **pkl** files are used for generating the final estimator predictions and the explainability images associated to each estimation. Each estimation can be done **for one by one input or any batch size** you want to put in the input csv files. So we can continue with the API configuration and deployment.

## API local releasing

First to configure the API releasing install the **postgresql** package.

```bash
apt install postgresql postgresql-*
```
Remember that this command will install the **postgresql** version associated to the latest (or currently installed) Linux distribution in your machine.

Subsequently, you must configure the database to do queries from the **fastAPI** session. Then, you need to modify the files on this absolute paths in Ubuntu:

- **/etc/postgresql/16/main/pg_hba.conf**
- **/etc/postgresql/16/main/postgresql.conf**

Take into account that this path will be different for another Linux distros, as well as for Mac and Windows. Search for the absolute locations of those files in your corresponding OS.

In the **pg_hba.conf** file you must change the line 118 and change the defaul method from **peer** to **md5**. 

![image](https://github.com/user-attachments/assets/d0a89b51-a783-4581-888d-efc558ff88ce)

And for the **postgresql.conf** you must change the line 60 uncommenting the line and changing the word  **localhost** for a *. This will allow the databse to read any IP not only the localhost.

![image](https://github.com/user-attachments/assets/0029c50f-4ae6-4bdb-ab01-f940603ad1dc)

After you modify this files and the corresponding please restart the **postgresql** service

```bash
service postgresql restart
```

Now, we can create the database associated to the default user **postgres** and set the password for the posgresql database. For this, we must first go to the **psql** terminal using the following command

```bash
sudo -u postgres psql
```

Next we must set the password, for this particular case, the password is **DataBase** but you can set your own password for convinience and parse it as an environment variable for security reasons. So you need to run the following command from the psql terminal.

```bash
ALTER USER postgres PASSWORD 'Password';
```

Now from outside the psql terminal, and being on your root terminal you must create the database name associated to the **postgres** like this.

```bash
createdb -U postgres apidb;
```

Now to finish the postgresql configuration just restart the service again. Then, you are ready to deploy the API from the local Python environment.

For this you just need to run the **app.py** file from the Titanic folder inside the APIs folder, you can check the code in detail [here](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/blob/main/APIs/Titanic/app.py).

Before running the API locally you must uncomment this line (at the end of the file) from the app.py and point the **upload** service on the fastAPI session from the localhost IP which is in most cases the 127.0.0.1.

![image](https://github.com/user-attachments/assets/74f9dab4-25ee-4f58-9024-99c7114713e6)

Now you can release the app using the following command.

```python
python app.py
```

if you go to any web-browser and you type: **127.0.0.1/upload** this will appear as the front-end input.

![image](https://github.com/user-attachments/assets/4616bc05-3dc2-47f4-89a5-e363396b01c7)

This form receives the **username**, **password** (that can be anything for the sake of the test). The left side div will show the ROC curve obtained after we run the notebook, the center part of the API contain the form objects, and the right part will contain the status message, the SHAP image associated with the estimation, and the link for the resulting **xls** files. The resulting exlainable images and xls can be seen in the [results](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/tree/main/APIs/Titanic/data) folder.

In the same way, and to be consistent with the input the user must define the input .csv files for estimation with the 11 features defined in the last part of the notebook for online training. Please, as user, save all the candidate inputs in the [input folder](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/tree/main/APIs/Titanic/inputs). Take into account because this kaggle AI service is not providing a preliminar normalization layer, therefore, the inputs of theee csv files must contain integers representing all the features described in notebook for offline training.

Then after you fill all the form and the SUBMIT button is activated, you can run the API and you will obtained the following results

![image](https://github.com/user-attachments/assets/0900ca76-f613-4605-b92b-50071b12e97e) 

If you click the link given by the API as the estimation results you can obtain an associated xls and explainer results in the  [results](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/tree/main/APIs/Titanic/data) folder.
Please observe that the xls and the explainability filenames are composed of a concatenation between the **username** the user has given as input in the forme, the random **ID** generated by the app, a random alphanumernic **code** generated by the app as well, the **model** name select by the user in the front, and the **date** (on the local machine) just after the estimation finishes.

![image](https://github.com/user-attachments/assets/ffaa6f63-b3ab-4830-aee5-9da07407725b)

if you open the resulting file in a xls reader as Excel or LibreOffice you will see the following output.

![image](https://github.com/user-attachments/assets/012fafc7-c2d5-42a3-b12f-2791f041d522)

In the first column you will see the index starting from zero to the last input (feature vectors) that the user must set for estimation, in the second column you will see estimation strings that is saying if the corresponding input (or the corresponding member of the Titanic crew) **survived (1) or not (0)**, the third column you can see the probability of the **no survive** class, and in the fourth column you ca see the probability of the **survive** class related to the model user has selected from the front. We can see for this particular example we hace 12 input vectors for clasifying (estimating).

Now after it finishes and you go to the results folder you must see the new files genearated in the result folder with the time it has been generated.

![image](https://github.com/user-attachments/assets/e112ef1a-5aad-4b8d-98a9-f50750d2cd07)

For checking the database you must go to **psql** and run this command:

```bash
psql -U postgres -d apidb
```

Now being in the **psql** terminal you must run the following commands and look for the last register associated to the last estimation that will be stored in the postgresql database

![image](https://github.com/user-attachments/assets/ec110a11-81b2-4bc3-9bc3-b28334768a40)



Now you can refresh the front-end page and you can run as many prediction you can for your own evaluation. Now, here are the steps to configure the **Docker** launching.

## API Docker

To run the docker deployment you need to first do a **docker-compose** and **build** of the image. If you go to the Titanic folder you can do it running simple the **docker_launch.sh** file as follows:

```bash
sh docker_launch.sh
```
To check the [docker-compose.yml](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/blob/main/APIs/Titanic/docker-compose.yml) and the [Dockerfile](https://github.com/meiyor/ABIChallenge_Juan_Manuel_Mayor_Torres/blob/main/APIs/Titanic/Dockerfile) you can go to any of these links


![image](https://github.com/user-attachments/assets/4ee2ffdc-b5ba-4e10-880e-b2a77b77d3e1)
