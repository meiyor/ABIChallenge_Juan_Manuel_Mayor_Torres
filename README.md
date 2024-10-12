# ABIChallenge_Juan_Manuel_Mayor_Torres
Infinita Consulting test for ML Engineer position

In This README we will describe the process for executing this API code locally and through **Docker** container. The steps outline for this execution will be:

- **Configuration**
- **Notebook Running (offline training)**
- **API local releasing**
- **API Docker**

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

After you are sure you have executed all the data debugging cells (in sequence), then you focused on the dataframe preparation, training, and models/training releasing at the end of the notebook.


