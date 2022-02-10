# pyISARICBasics

This package is intended to be a gentle introduction to the ISARIC dataset with the goal of helping researchers access and become familiar with the ISARIC dataset. 

The package is in the early stages of development. 


# Install 
This package can be installed using pip - the package installer for Python. We suggest creating a virtual environment (using conda or otherwise). Miniconda (https://docs.conda.io/en/latest/miniconda.html) is a minimal installer for Anaconda that is suitable for this purpose. 

Once you have installed conda it is simple as creating a new virtual environment (https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). 

Once you have activated your new virtual environment you can then type: 
		
		pip install pyisaricbasics

You can then access any functionality described in the documentation in any IDE or Jupyter Notebook configured to use this environment. 

# Tutorial 
Once you have created a virtual environment to access the tutorial you can download the .ipynb file from this repo. Create a folder that contains this notebook and another folder containing the raw ISARIC data. For ease of use we suggest renaming the individual .csv's to only contain their domain names. E.g. "SA.csv" for the SA domain or "IN.csv" for the IN domain. 

If you then activate your virtual environment and navigate to your newly created folder you can type: 

		jupyter notebook
Which will launch an interactive browser window. You can then open the tutorial notebook. 

# Documentation 

Package documentation is contained at the following link: https://kyleyoung1997.github.io/pyISARICBasics/
