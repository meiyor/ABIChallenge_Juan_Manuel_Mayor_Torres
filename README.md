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
jupyter notebook --allow-root
```

You can change and set your environment clicking on the Kernel menu of jupyter here:

![image](https://github.com/user-attachments/assets/a84dcff4-7a26-4702-9589-1cf9da53cef3)
