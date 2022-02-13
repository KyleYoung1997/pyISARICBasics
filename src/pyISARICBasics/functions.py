import gc
import os
import sqlite3
import pandas as pd
import numpy as np

ALL_DOMAINS = {"DM", "DS", "ER", "HO", "IE", "IN", "LB", "MB", "RP", "RS", "SA", "SV", "VS", "CQ", "SC", "PO", "TI"}
"""
A set containing all possible domains in the ISARIC dataset. 
"""


### TODO write custom .hdf5 loader and saver functions for QUICKEST I/O
### This could be tricky -> it seems like the best option is to convert dtypes from object to pandas d types
### but then we need to handle stuff differently in other places in code...
### We also need to try and deal with the fact that it seems like df.to_hdf() freaks out with DF's over a certain size
### You can load and append using hdf but I am not sure how yet -> you can also query using hdf this is definitely worth
### looking into though.

def csv_to_sqlite(data_folder, db_file, overwrite=True):
    """
    Converts all raw .csv files to a sqlite database

    :param data_folder: Location of folder where data is contained

    :param db_file: Name of sqlite databse within data_folder

    :param overwrite: Rewrite sqlite database if it already exists

    :return: Null
    """
    # if os.path.isfile(os.path.join(data_folder, db_file)):
    #     print("Database already exists")
    #     return
    for file in os.listdir(data_folder):  # get all files in data_folder
        if file.endswith(".csv"):  # get csv files
            name = os.path.splitext(file)[0]  # file name with no extension
            print(name)
            name = parse_domain_names(name)
            name = name.replace('-', '_')  # replace - with _ to avoid sql errors.
            print("_" * 150)
            print("Creating table:", name)
            file_path = os.path.join(data_folder, file)

            df = pd.read_csv(file_path, on_bad_lines='skip', verbose=False)
            df = df.rename(columns=lambda x: x.strip())
            # print(df.dtypes)
            # df = df.convert_dtypes()
            #
            # print(df.dtypes)
            print("Length of df ", name, len(df))
            df_to_sqlite(df, name, data_folder, db_file, overwrite)
            del df
            gc.collect()


def df_to_sqlite(df, table_name, data_folder, data_file, overwrite=True):
    """
    Creates a table in sqlite database using the supplied dataframe, also saves .pickle files for each table saved to
    the sql database (these are much quicker to load in to memory using Python and Pandas).

    :param df: Dataframe to convert to sqlite table

    :param table_name: Table name of dataframe (to be saved as in database)

    :param data_folder: Location of folder where data is contained

    :param data_file: db_file: Name of sqlite database within data_folder

    :param overwrite: overwrite: Rewrite sqlite database if it already exists

    :return: True, if write successful
    """
    # Executes a query and returns a pandas dataframe
    # query is a string.
    # data_folder is the folder that sqlite file is in.
    # data_file is the name of sqlite file.
    if overwrite:
        if_exists = 'replace'
    else:
        if_exists = None
    try:
        db_file = os.path.join(data_folder, data_file)
        con = sqlite3.connect(db_file)  # connection to the database file
        df.to_sql(table_name, con, if_exists=if_exists, index=False)
        save_string = os.path.join(data_folder, f"{table_name}.pickle")
        df.to_pickle(save_string)
        del df
        gc.collect()
        return True
    except ValueError as e:
        print("Table already exists in database, set Overwrite = True if you wish to overwrite existing table.")
        return None
    finally:
        con.close()


def parse_domain_names(name: str) -> str:
    """
    Function to read domain name and return two letter abbreviation for each domain

    :param name: (str) filename similar to "Partner_DM_2021-09-20.csv"

    :return: (str) Two letter abbreviated domain name e.g. "DM" for above filename
    """
    domain = [i for i in name.split("_") if i in ALL_DOMAINS]
    if len(domain) > 1:
        print("Couldn't parse domain name from filename returning full path as domain name")
        return name
    else:
        return domain.pop()
