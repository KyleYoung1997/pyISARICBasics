import gc
import os
import sqlite3

import numpy as np
import pandas as pd
from . import functions

# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)


class Domain:
    """
    A generic class that loads a domain and provides basic exploratory data analysis
    """

    def __init__(self, domain: str, data_directory: str, num_rows = None):

        # Load domain as a dataframe and store as a class field
        self.frame = self.read_domain(domain, data_directory, num_rows)
        """
        A Pandas DataFrame which is the data structure where we store the information about this domain. 
        """
        # Store the name of domain as a class field
        self.domain = domain
        """
        A string that contains the name of the domain that we have currently loaded. 
        """

        # We handle term based domains slightly different
        if domain in ['HO', 'SA', 'IN']:
            # Save term based domain information as a protected attribute - we use this behind the scenes
            self.__is_term_outcome = True
            # Process outcome column - this is appended to the end of our class specific frame object
            self.process_occur()
        else:
            self.__is_term_outcome = False

    @staticmethod
    def __read_domain_deprecated(domain, data_folder, data_file):
        """

        :param domain: Domain to load e.g. DM, SA, IN
        :param data_folder: Directory where database is located
        :param data_file: Filename of sqlite database
        :return: dataframe that contains the whole domain
        """

        try:
            db_file = os.path.join(data_folder, data_file)
            con = f'sqlite:///{db_file}'
            # con = sqlite3.connect(db_file)
            # df = pd.read_sql_table(domain, uri)
            if domain == "SA":
                columns = "STUDYID, USUBJID, SASEQ, SADY, SATERM, SAMODIFY, SACAT, SAPRESP, SAOCCUR"
            elif domain == "IN":
                columns = "USUBJID, INSEQ, INDY, INSTDY, INTRT, INMODIFY, INCAT, INPRESP, INOCCUR, INREFID"
                # columns = "*"
            else:
                columns = "*"
            df = pd.read_sql("SELECT {} FROM '{}'".format(columns, domain), con)
            df = df.rename(columns=lambda x: x.strip())
            return df

        except Exception as e2:
            print("Domain could not be loaded from sqlite database", e2)
            return
        finally:
            print("Domain {} Loaded".format(domain))
            # con.close()
            gc.collect()

    @staticmethod
    def read_domain(domain: str, data_folder: str, num_rows: int) -> pd.DataFrame:
        """
        Loads a domain from auxiliary generated pickle files for faster Python I/O than with SQL table reads

        :param num_rows: Integer (optional): Number of rows to load from dataframe (default loads all)

        :param domain: String name of domain

        :param data_folder: String, Path to folder containing .pickle files

        :return: pd.DataFrame containing the full domain (all columns and rows)
        """
        db_file = os.path.join(data_folder, domain)
        df = pd.read_pickle(f"{db_file}.pickle")

        if num_rows is None:
            return df
        else:
            return df[:num_rows]

    def columns(self):
        """

        :return: prints list of columns contained in self.frame
        """
        print(self.frame.columns.to_list())

    def exclude_columns(self, columns: list):
        """
        Excludes some columns from the class variable 'frame'

        :param columns: Columns to drop from domain

        :return: None (operates on class variable)
        """
        try:
            self.frame.drop(labels=columns, axis=1, inplace=True)
        except KeyError:
            print(print(f"At leas one column: '{columns}' is not in the current domain: '{self.domain}'"))

    def include_columns(self, columns: list):
        """

        :param columns: (list) Columns to include in dataframe.

        :return: None (operates on class variable)
        """
        try:
            self.frame = self.frame[columns]
        except KeyError:
            print(print(f"At leas one column: '{columns}' is not in the current domain: '{self.domain}'"))

    def column_events(self, column: str):
        try:
            print(self.frame[column].unique())
        except KeyError:
            print(f"Column '{column}' is not in the current domain: '{self.domain}'")

    def select_variable_from_column(self, column: str, variable: str) -> pd.DataFrame:
        """
        Filters and returns a dataframe based off column and variable information, Returns an error if column is not
        found within the current domain.

        :param variable: String containing variable to be selected from column

        :param column: String containing the column within self.frame to selct variable from

        :return: Filtered dataframe containing only entries where self.frame[column] contains the value of variable
        """
        try:
            df = self.frame[self.frame[column] == variable]
            if len(df) == 0:
                print(f"There were no occurences of {variable} within {column}")
            return df
        except KeyError as e:
            print(f"Column '{column}' is not in the current domain: '{self.domain}'")

    def table_missingness(self, column=None, variable=None):

        """
        Print's a missingness table for either a whole table, or a filtered table where we have selected
        frame.column == variable

        :param column: (optional) column to search for term variable

        :param variable: (optional) variable to search for

        :return: None
        """
        if variable is None and column is None:
            n_unique = self.frame.USUBJID.nunique()
            print(f"Total number of rows: {len(self.frame)}")
            print(f"Total number of unique patients: {n_unique}")
            print(self.frame.isna().sum())
        elif column is None or variable is None:
            print("Must specify both a column and a variable or neither")
        else:
            try:
                trimmed = self.frame[self.frame[column] == variable]
                n_unique = trimmed.USUBJID.nunique()
                print(f"Total number of rows: {len(trimmed)}")
                print(f"Total number of unique patients: {n_unique}")
                print(trimmed.isna().sum())
            except KeyError as e:
                print(f"Column '{column}' is not in the current domain: '{self.domain}'")

    def column_summary(self, column: str,  *variables, proportions=False, status=False,):
        """



        :param column: String, Column name

        :param variables: String, optional name of variables to filter by

        :param status: If True, include Y, N or U information from self.frame.status

        :param proportions: Boolean: If True print normalised proportions for items in column, by default: False returns
        counts of events in column.

        :return:
        """
        try:
            # Loads column as pd.Series
            if len(variables) == 0:
                filtered = self.frame[column]
                status_filt = self.frame['status']
            else:
                filtered = self.frame[column]
                mask = filtered.isin(variables)
                filtered = filtered[mask]
                status_filt = self.frame['status'][mask]

            if status:
                with pd.option_context('display.max_rows', None):
                    print((filtered + "__" + status_filt).value_counts(normalize=False).sort_index())
            else:
                with pd.option_context('display.max_rows', None):
                    print(filtered.value_counts(normalize=proportions))
        except KeyError as e:
            print(f"Column '{column}' is not in the current domain: '{self.domain}'")

    def process_occur(self):
        """
        Protected method that processes the XXOCCUR, XXPRESP into Y, N or U outcomes. Modifies the class dataframe and
        maps variables according to the following logic:


        | xxPRESP | xxOCCUR | status |
        |---------|---------|--------|
        | NA      | NA      | Y      |
        | NA      | Y       | U      |
        | N       | Y       | N      |
        | U       | Y       | U      |
        | Y       | NA      | Y      |
        | Y       | Y       | Y      |

        :return: None
        """

        if not self.__is_term_outcome:
            pass
        else:
            occur = f"{self.domain}OCCUR"
            presp = f"{self.domain}PRESP"
            yes_maps = (self.frame[occur] == 'Y')

            no_maps = self.frame[occur] == 'N'
            yes_maps = (self.frame[occur].isna() & self.frame[presp].isna()) | (self.frame[presp] != 'Y') | (yes_maps)
            unknown_maps = (self.frame[occur].isna() & (self.frame[presp] == "Y")) | (self.frame[occur] == 'U')

            conds = [yes_maps, no_maps, unknown_maps]
            choices = ["Y", "N", "U"]

            self.frame["status"] = np.select(conds, choices, None)

    def free_text_search(self, *term: str) -> pd.DataFrame:
        """
        Searches for free text entries and returns a filtered dataframe with rows where there is a free text match

        :param term: A string search term or (list). We search for any occurences of this substring e.g. term 'hospital' would
        also return rows with a free text entry matching 'hospitalization'. This function is NOT case sensitive

        :return: A filtered df with rows containing 'term' in the relevant column of the original domain
        """

        if self.domain not in ['SA', 'IN', 'HO', 'LB']:
            print("Free text search is currently only implemented for SA, IN, LB or HO domains")
            print(f"You have currently loaded '{self.domain}'")
            return

        domain_free_text = {"HO": "HOTERM", "IN": "INTRT", "SA": "SATERM", "LB":"LBTEST"}
        search_col = domain_free_text[self.domain]
        try:
            search_col_mask = self.frame[search_col].str.contains('|'.join(term), case=False, na=False)
            filtered_frame = self.frame[search_col_mask]
            readable_terms = " or ".join(term)
            print(f"Free text entries containing any of {readable_terms} were found in {len(filtered_frame)} rows")
        except TypeError:
            print("This function requires the 'term' argument to be a string")
            filtered_frame = None
        # we probably only want to return some filtered columns here (e.g. derived term, dy, seq, outcoke

        return filtered_frame

    def save_to_sqlite(self, name: str, data_directory: str, database_file: str):
        """

        :param name: (string) Name of domain we are overwriting / saving

        :param data_directory: (string) path to data directory

        :param database_file: (string) name of database file

        :return: True, if write successful

        """
        functions.df_to_sqlite(self.frame, name, data_directory, database_file)
