import gc
import os
import sqlite3
import pandas as pd
import numpy as np


###TODO write custom .hdf5 loader and saver functions for QUICKEST I/O

def csv_to_sqlite(data_folder, db_file, overwrite=True):
    # if os.path.isfile(os.path.join(data_folder, db_file)):
    #     print("Database already exists")
    #     return
    for file in os.listdir(data_folder):  # get all files in data_folder
        if file.endswith(".csv"):  # get csv files

            name = os.path.splitext(file)[0]  # file name with no extension
            name = name.replace('-', '_')  # replace - with _ to avoid sql errors.
            print("_" * 150)
            print("Creating table:", name)
            file_path = os.path.join(data_folder, file)

            df = pd.read_csv(file_path, on_bad_lines='skip', verbose = False)
            df = df.rename(columns=lambda x: x.strip())
            # print(df.dtypes)
            # df = df.convert_dtypes()
            #
            # print(df.dtypes)
            print("Length of df ", name, len(df))
            df_to_sqlite(df, name, data_folder, db_file, overwrite)
            save_string = os.path.join(data_folder, f"{name}.pickle")
            df.to_pickle(save_string)
            del df
            gc.collect()

def df_to_sqlite(df, table_name, data_folder, data_file, overwrite=True):
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
        del df
        gc.collect()
        return True
    except ValueError as e:
        print("Table already exists in database, set Overwrite = True if you wish to overwrite existing table.")
        return None
    finally:
        con.close()


# def read_domain(domain, data_folder, data_file):
#     """
#
#     :param domain: Domain to load e.g. DM, SA, IN
#     :param data_folder: Directory where database is located
#     :param data_file: Filename of sqlite database
#     :return: dataframe that contains the whole domain
#     """
#     try:
#         db_file = os.path.join(data_folder, data_file)
#
#         con = sqlite3.connect(db_file)
#         # df = pd.read_sql_table(domain, uri)
#         df = pd.read_sql("SELECT * FROM '{}'".format(domain), con)
#         df = df.rename(columns=lambda x: x.strip())
#
#         return df
#
#     except Exception as e2:
#         print("Domain could not be loaded from sqlite database", e2)
#         return
#     finally:
#         print("Domain {} Loaded".format(domain))
#         con.close()


# def read_cols_from_domain(domain, cols, data_folder, data_file):
#     try:
#         db_file = os.path.join(data_folder, data_file)
#
#         if len(cols) == 0:
#             cols = '*'
#         else:
#             cols = ",".join(cols)
#
#         con = sqlite3.connect(db_file)
#
#         df = pd.read_sql("SELECT {} FROM '{}'".format(cols, domain), con)
#         df = df.rename(columns=lambda x: x.strip())
#
#         print("Domain {} Loaded".format(domain))
#         return df
#
#     except Exception as e2:
#         print("Exception: ", e2)
#         return
#     finally:
#
#         con.close()





