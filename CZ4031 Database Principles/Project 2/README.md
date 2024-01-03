# CZ4031 Project 2

## Prerequisites

Python 3.11 was used during development and is recommended. 3.10 should be the minimum as structural pattern matching is used.

The following packages are required to be installed

```
pip install psycopg2
pip install python-dotenv
pip install pysimplegui 
pip install networkx[default] 
pip install pydot 
```

### External Dependencies

[Graphviz](https://www.graphviz.org/download/) is used to display the QEP graph. Ensure the directory containing `dot` executable is in the PATH variable.

If installed using the installer, ensure `C:\Program Files\Graphviz\bin` exists and is in your PATH variable


## Running project.py

A `.env` file is required for setting up connection with the database with the values below. Ensure `DB_NAME` is the database holds the dataset you wish to query and that the `.env` file is in the same directory as `project.py`.

```
DB_NAME=xxx
DB_USER=xxx
DB_PASSWORD=xxx
DB_HOST=localhost
DB_PORT=5432
```

The project is started by simply calling 

```
python project.py
```
