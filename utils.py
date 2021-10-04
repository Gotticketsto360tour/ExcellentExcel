# import the pandas module and call it pd - we wont need anything else
import pandas as pd

# read the excel file - can be changed to any xlsx file
# NOTE: ../ just means "go one back from where you are now"

# xls = pd.ExcelFile("../data/alexander/Arkitektskolen-Aarhus-2021.xlsx")
# xls = pd.ExcelFile("../data/alexander/NKS-til-forskere.xlsx")


def check_if_in_dict(value, dictionary):
    """Function for checking whether value already
    exists in the dictionary. If it does, replace with
    value_1

    Args:
        value (str): string containing a name of a column
        dictionary (dict): dictionary containing the values

    Returns:
        [str]: value of column name
    """
    if value in dictionary.values():
        return check_if_in_dict(value + "_1", dictionary)
    else:
        return value


def fill_rename_dict(x, dictionary):
    """Fills the rename dictionary - uses the
    "check_if_in_dict" to avoid duplicates.
    Intended use is with pandas "apply"-method.

    Args:
        x (row): row in a pandas DataFrame
        dictionary (dict): Dictionary for renaming
    """
    value = check_if_in_dict(x[1], dictionary)
    dictionary[x[0]] = value
    return value


def fill_value_dict(df1):
    """Value for filling in the mapping dictionary

    Args:
        df1 (pd.DataFrame): Dataframe containing the information on names

    Returns:
        [dict]: nested dictionary where first level is the name of the column,
        and the second level is the mapping for the column
    """
    # list all the column names
    question_col = df1["key_column"].values
    # initialize empty dictionary
    value_dict = {}

    # loop over all questions
    for question in question_col:
        # subset the data so they only contain row containing
        # the relevant information.
        # NOTE: [0][2:] unpacks the list and takes all elements after the second element
        subset = df1[df1["key_column"] == question].values[0][2:]

        # take the last element (the key column)
        name = subset[-1]

        # insert the mapping in the value dictionary
        # NOTE: check e==e is to exclude na's and e should not be the name of the column
        value_dict[name] = {
            i + 1: e for i, e in enumerate(subset) if e == e and e != name
        }

    return value_dict


def use_dict(x, value_dict, value):
    """Function for making sure not to overwrite
    based on mapping

    Args:
        x (str): answer to a question
        value_dict (dict): value dictionary containing names and mapping
        value (str): name of the column

    Returns:
        str: Either the original answer or mapped answer
    """
    if value_dict[value].get(x):
        return value_dict[value].get(x)
    else:
        return x


def get_sheets_from_excel(path_to_excel):
    xls = pd.ExcelFile(path_to_excel)
    return xls.sheet_names


def excel_helper(path_to_excel, language):
    xls = pd.ExcelFile(path_to_excel)
    # split into two different dataframes
    df1 = pd.read_excel(xls, language)
    df2 = pd.read_excel(xls, "Data")

    # FIRST: We want to rename df2 on the basis of the values of
    # the two first columns in df1

    # get all columns from df1
    cols = df1.columns

    # take the first 2, we wont need anything else
    rename_dict_df = df1[cols[0:2]]

    # initialize an empty dictionary to store the values
    rename_dict = {}

    # apply the function on all rows in dataframe and log them in
    # the column "key_column"
    df1["key_column"] = rename_dict_df.apply(
        lambda x: fill_rename_dict(x, rename_dict), axis=1
    )

    # rename df2 on the basis of the rename dictionary
    df2 = df2.rename(columns=rename_dict)

    # use the function to create the mapping
    value_dict = fill_value_dict(df1)

    # loop over column names
    for value in value_dict:
        # check if this mapping makes sense
        if value in list(df2.columns):
            try:
                df2[value] = df2[value].apply(lambda x: use_dict(x, value_dict, value))
            except Exception as e:
                print(f"Ups! Something went wrong at the column named {value}")
                print(f"Contact Mikkel and tell him the following went wrong: {e}")

    return value_dict, df2


if __name__ == "__main__":
    excel_helper("../data/alexander/NKS-til-forskere.xlsx").to_csv("test.csv")
