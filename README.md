# pyISARICBasics

This package is intended to be a gentle introduction to the ISARIC dataset with the goal of helping researchers access and become familiar with the ISARIC dataset. 

The package is in the early stages of development and feature requests are welcomed as are new contributors. If you would like to contribute please make contact! 


# Install 
This package can be installed using pip - the package installer for Python. We suggest creating a virtual environment (using conda or otherwise). Miniconda (https://docs.conda.io/en/latest/miniconda.html) is a minimal installer for Anaconda that is suitable for this purpose. 

Once you have installed conda you will need to create a new virtual environment. The steps are as follows (but see https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html for alternatives). 

Type the following into a console window: 


	conda create -n "your_env_name" python=3.8
	
	
This will create a new conda environment with Python 3.8.

You should then activate your new environment by entering the following command: 

	conda activate "your_env_name" 
	
You then need to install pip using the following command: 
	
	conda install pip

You can then type the following command to install the package: 
		
	pip install pyISARICBasics

You can then access any pyISARICBasics functionality described in the documentation using IDE or Jupyter Notebook that is configured to use this environment. 

While the package is in early development we suggest regularly checking for updates with the following command:

	pip install pyISARICBasics --upgrade

# Documentation 

Package documentation is contained at the following link: https://kyleyoung1997.github.io/pyISARICBasics/


# Tutorial 
Once you have created a virtual environment to access the tutorial you can download the .ipynb file from this repo. 

Create a folder that contains this notebook and another folder containing the raw ISARIC data. 

You then need to navigate to your newly created folder and activate your virtual environment. To do this you need to open a console window and use the following command: 

	cd "path_to_directory" 
	
(If you're using a mac you can type cd and then drag the folder icon of your newly created folder into the terminal window to get the path) 

Then type the following command to open jupyter notebook: 

	jupyter notebook
		
Which will launch an interactive browser window. You can then open the tutorial notebook. 

