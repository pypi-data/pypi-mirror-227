# Import necessary packages here
import json
import logging
import logging.handlers
import os
import xml.etree.ElementTree as ET
from collections import deque
from typing import Any, Union

import pandas as pd
import pdfplumber
import xmltodict
import yaml

# ==========================================================================================
# ==========================================================================================

# File:    io.py
# Date:    July 09, 2023
# Author:  Jonathan A. Webb
# Purpose: This file contains classes and functions that can be used to read and write
#          to files
# ==========================================================================================
# ==========================================================================================
# Insert Code here


class ReadKeyWords:
    """
    This class can be used by a read to read a text based config file.  The methods
    will look for a specific key word that must begin on the first character of each
    line, and will read in the variable or variables just to the right of the
    keyword as a user specified data type.  The user can also print the object
    which will display the user specified number of lines on the screen.

    This class is cabale of reading files that contain text, json and xml
    data in one file.  In addition, this class can read files that are entirely
    compriesd of text, json, or xml data.

    :param file_name: The file name to be read including the path length
    :param print_lines: The number of lines to be printed to the screen if the
                        user prints an instance of the class. Defaulted to 50
    :raises FileNotFoundError: If the file does not exist

    Example file titled test_key_words.txt

    .. literalinclude:: ../../../data/test/text_key_words.txt
       :language: text

    .. code-block:: python

        # Instantiate the class
        reader = ReadKeyWords("test_key_words.txt", print_lines=2)

        # Print the instance, displaying 2 lines
        print(reader)

        >> Float Value: 4.387 # Comment line not to be read
        >> Double Value: 1.11111187 # Comment line not to be read

    The user can also adjust the print_lines attribute after instantiation
    if they wish to change the number of printed lines

    """

    def __init__(self, file_name: str, print_lines: int = 50):
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"FATAL ERROR: {file_name} does not exist")
        self._file_name = file_name
        self.__lines = self._read_lines()
        self.print_lines = print_lines

    # ------------------------------------------------------------------------------------------

    def read_variable(self, keyword: str, data_type: type) -> Any:
        """
        Search each line for the specified keyword and read the variable to the
        right of the keyword as the specified data type

        :param keyword: The keyword to search for in each line.
        :param data_type: The data type to be used in order to casy the variable
        :return: The float variable to the right of the keyword.
        :raises ValueError: If the keyword is not found or if the variable cannot
                            be parsed as a float.

        .. code-block:: python

           import numpy as np
           # Instantiate the class
           reader = ReadKeyWords("test_key_words.txt")
           value = reader.read_variable("Double Value:", np.float32)
           print(value)
           print(type(value))

           >> 1.11111187
           >> <class 'numpy.float32'>

        However, be carefult with strings.  This method will only read the first
        character array following the key word. In order to read in the entire
        line as a string, use the read_string_variable method.

        .. code-block:: python

           # Instantiate the class
           reader = ReadKeyWords("test_key_words.txt")
           value = reader.read_variable("String:", str)
           print(value)
           print(type(value))

           >> "Hello"
           >> str
        """
        for line in self.__lines:
            if line.startswith(keyword):
                value_str = line[len(keyword) :].strip()
                try:
                    return data_type(value_str)
                except ValueError:
                    raise ValueError(f"Invalid float value found for {keyword}")
        raise ValueError(f"Keyword '{keyword}' not found in the file")

    # ------------------------------------------------------------------------------------------

    def read_string_variable(self, keyword: str) -> str:
        """
        Search each line for the specified keyword and read the string variable
        to the right of the keyword.

        :param keyword: The keyword to search for in each line.
        :return: The string variable to the right of the keyword.
        :raises ValueError: If the keyword is not found.

        .. code-block:: python

           # Instantiate the class
           reader = ReadKeyWords("test_key_words.txt")
           value = reader.read_variable("String:", str)
           print(value)
           print(type(value))

           >> Hello # Comment to be read
           >> str
        """
        for line in self.__lines:
            if line.startswith(keyword):
                return line[len(keyword) :].strip()
        raise ValueError(f"Keyword '{keyword}' not found in the file")

    # ------------------------------------------------------------------------------------------

    def read_list(self, keyword: str, data_type: type) -> list[Any]:
        """
        Search each line for the specified keyword and read the values after the keyword
        as a list of the user-defined data type.

        :param keyword: The keyword to search for in each line.
        :param data_type: The data type to which the values should be transformed.
        :return: The list of values after the keyword, transformed into the specified
                 data type.
        :raises ValueError: If the keyword is not found.

        .. code-block:: python

           # Instantiate the class
           reader = ReadKeyWords("test_key_words.txt")
           value = reader.read_list("Float List:", float)
           print(value)

           >> [ 1.1, 2.2, 3.3, 4.4 ]
        """
        for line in self.__lines:
            if line.startswith(keyword):
                tokens = line.split()[2:]  # Skip the keyword and colon
                try:
                    values = [data_type(token) for token in tokens]
                    return values
                except ValueError:
                    raise ValueError(
                        f"Invalid {data_type.__name__} value found for {keyword}"
                    )
        raise ValueError(f"Keyword '{keyword}' not found in the file")

    # ------------------------------------------------------------------------------------------

    def read_json(self, keyword: str) -> dict:
        """
        Search each line for the specified keyword and read the JSON data
        to the right of the keyword until the termination of brackets.

        :param keyword: The keyword to search for in each line.
        :return: The JSON data as a dictionary.
        :raises ValueError: If the keyword is not found or if the JSON data is not valid.

        .. code-block:: python

           # Instantiate the class
           reader = ReadKeyWords("test_key_words.txt")
           value = reader.read_json("JSON Data:")
           print(value)

           >> {"book": "History of the World", "year": 1976}
        """
        found_keyword = False
        json_data = ""
        for line in self.__lines:
            if line.startswith(keyword):
                found_keyword = True
                json_data += line.split(keyword)[-1].strip()
                if json_data.startswith("{") and json_data.endswith("}"):
                    try:
                        return json.loads(json_data)
                    except json.JSONDecodeError:
                        raise ValueError(f"Invalid JSON data for keyword '{keyword}'")

        if not found_keyword:
            raise ValueError(f"Keyword '{keyword}' not found in the file")
        else:
            raise ValueError(f"Invalid JSON data for keyword '{keyword}'")

    # ------------------------------------------------------------------------------------------

    def read_full_json(self, keyword: str = None) -> Union[dict, list]:
        """
        Read the entire contents of the file as JSON data.
        If a keyword is provided, search for that keyword and return the nested
        dictionaries beneath it.

        :param keyword: The keyword to search for in the file. If None,
                        returns the entire JSON data.
        :return: The JSON data as a dictionary or list.
        :raises ValueError: If the keyword is specified but not found
                            in the file.

        Unlike the read_json method, this method assumes the entire file is
        formatted as a .json file.  This method will allow a user to read
        in the entire contents of the json file as a dictionary, or it
        will read in the dictionaries nested under a specific key word.
        If you assume the input file titled example.json has the following
        format

        .. code-block:: json

           {
            "key1": "value1",
            "key2": {
                "subkey1": "subvalue1",
                "subkey2": {
                    "subsubkey1": "subsubvalue1",
                    "subsubkey2": "subsubvalue2"
                 }
              }
           }

        The code to extract data would look like:

        .. code-block:: python

           reader = ReadKeyWords("example.json")
           value = reader.read_full_json()
           print(value)

           >> {
               "key1": "value1",
               "key2": {
                   "subkey1": "subvalue1",
                   "subkey2": {
                       "subsubkey1": "subsubvalue1",
                       "subsubkey2": "subsubvalue2"
                   }
               }
           }

           new_value = reader.read_full_json("subkey2")
           print(new_value)
           >> {"subsubkey1": "subsubvalue1", "subsubkey2": "subsubvalue2"}
        """
        json_data = json.loads("\n".join(self.__lines))

        if keyword is None:
            return json_data

        def find_nested_dictionaries(data, keyword):
            if isinstance(data, dict):
                if keyword in data:
                    return data[keyword]
                for value in data.values():
                    result = find_nested_dictionaries(value, keyword)
                    if result is not None:
                        return result
            elif isinstance(data, list):
                for item in data:
                    result = find_nested_dictionaries(item, keyword)
                    if result is not None:
                        return result
            return None

        result = find_nested_dictionaries(json_data, keyword)
        if result is not None:
            return result
        else:
            raise ValueError(f"Keyword '{keyword}' not found in the JSON data")

    # ------------------------------------------------------------------------------------------

    def read_xml(self, keyword: str) -> dict:
        """
        Search each line for the specified keyword and read the XML data
        to the right of the keyword until the termination of tags.

        :param keyword: The keyword to search for in each line.
        :return: The XML data as a dictionary.
        :raises ValueError: If the keyword is not found or if the XML data is not valid.
        """
        found_keyword = False
        xml_data = ""
        for line in self.__lines:
            if line.startswith(keyword):
                found_keyword = True
                xml_data += line.split(keyword)[-1].strip()
                if xml_data.startswith("<") and xml_data.endswith(">"):
                    try:
                        return xmltodict.parse(xml_data)
                    except xmltodict.ParsingInterrupted:
                        raise ValueError(f"Invalid XML data for keyword '{keyword}'")

        if not found_keyword:
            raise ValueError(f"Keyword '{keyword}' not found in the file")
        else:
            raise ValueError(f"Invalid XML data for keyword '{keyword}'")

    # ------------------------------------------------------------------------------------------

    def read_full_xml(self, keyword: str = None):
        """
        Read the XML data. If a keyword is provided, search for the specified
        keyword in the XML data and return the nested elements beneath it.
        If no keyword is provided, return the full XML data.

        :param keyword: The keyword to search for in the XML data.
        :return: The XML data as a dictionary object or the nested elements
                 as an ElementTree object if a keyword is provided.
        :raises ValueError: If the keyword is specified but not found in the XML data.

        If you assume the input file titled example.xml has the following format:

        .. code-block:: xml

           <root>
               <key1>value1</key1>
               <key2>
                   <subkey1>subvalue1</subkey1>
                   <subkey2>
                       <subsubkey1>subsubvalue1</subsubvalue1>
                       <subsubkey2>subsubvalue2</subsubvalue2>
                   </subkey2>
               </key2>
           </root>

        The code to extract data would look like:

        .. code-block:: python

           reader = ReadKeyWords("example.xml")
           value = reader.read_full_xml()
           print(value)

           >> {
               "root": {
                   "key1": "value1",
                   "key2": {
                       "subkey1": "subvalue1",
                       "subkey2": {
                           "subsubkey1": "subsubvalue1",
                           "subsubkey2": "subsubvalue2"
                       }
                   }
               }
           }

           new_value = reader.read_full_xml("subkey2")
           print(new_value)
           >> {
               "subkey1": "subvalue1",
               "subkey2": {
                   "subsubkey1": "subsubvalue1",
                   "subsubkey2": "subsubvalue2"
               }
           }
        """
        tree = ET.parse(self._file_name)
        root = tree.getroot()
        if keyword is None:
            xml_string = ET.tostring(root, encoding="utf-8").decode()
            return xmltodict.parse(xml_string)
        else:
            elements = root.findall(f".//{keyword}")
            if elements:
                xml_string = ET.tostring(elements[0], encoding="utf-8").decode()
                return xmltodict.parse(xml_string)
            else:
                raise ValueError(f"Keyword '{keyword}' not found in the XML data")

    # ==========================================================================================
    # PRIVATE-LIKE methods

    def _read_lines(self):
        """
        This private method will read in all lines from the text file
        """
        with open(self._file_name) as file:
            lines = [line.strip() for line in file]
        return lines

    # ------------------------------------------------------------------------------------------

    def __str__(self):
        """
        This private method determines how many of the lines are to be printed to
        screen and pre-formats the data for printing.
        """
        num_lines = min(self.print_lines, len(self.__lines))
        return "\n".join(self.__lines[:num_lines])


# ==========================================================================================
# ==========================================================================================
# READ COLUMNAR DATA


def read_csv_columns_by_headers(
    file_name: str, headers: dict[str, type], skip: int = 0
) -> pd.DataFrame:
    """

    :param file_name: The file name to include path-link
    :param headers: A dictionary of column names and their data types.
                    types are limited to ``numpy.int64``, ``numpy.float64``,
                    and ``str``
    :param skip: The number of lines to be skipped before reading data
    :return df: A pandas dataframe containing all relevant information
    :raises FileNotFoundError: If the file is found to not exist

    This function assumes the file has a comma (i.e. ,) delimiter, if
    it does not, then it is not a true .csv file and should be transformed
    to a text function and read by the read_text_columns_by_headers function.
    Assume we have a .csv file titled ``test.csv`` with the following format.

    .. list-table:: test.csv
      :widths: 6 10 6 6
      :header-rows: 1

      * - ID,
        - Inventory,
        - Weight_per,
        - Number
      * - 1,
        - Shoes,
        - 1.5,
        - 5
      * - 2,
        - t-shirt,
        - 1.8,
        - 3,
      * - 3,
        - coffee,
        - 2.1,
        - 15
      * - 4,
        - books,
        - 3.2,
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_csv_columns_by_headers

       > file_name = 'test.csv'
       > headers = {'ID': int, 'Inventory': str, 'Weight_per': float. 'Number': int}
       > df = read_csv_columns_by_headers(file_name, headers)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40

    This function can also use the `skip` attributed read data when the
    headers are not on the first line.  For instance, assume the following csv file;

    .. list-table:: test1.csv
      :widths: 16 8 5 5
      :header-rows: 0

      * - This line is used to provide metadata for the csv file
        -
        -
        -
      * - This line is as well
        -
        -
        -
      * - ID,
        - Inventory,
        - Weight_per,
        - Number
      * - 1,
        - Shoes,
        - 1.5,
        - 5
      * - 2,
        - t-shirt,
        - 1.8,
        - 3,
      * - 3,
        - coffee,
        - 2.1,
        - 15
      * - 4,
        - books,
        - 3.2,
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_csv_columns_by_headers

       > file_name = 'test1.csv'
       > headers = {'ID': int, 'Inventory': str, 'Weight_per': float, 'Number': int}
       > df = read_csv_columns_by_headers(file_name, headers, skip=2)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found")
    head = list(headers.keys())
    df = pd.read_csv(file_name, usecols=head, dtype=headers, skiprows=skip)
    return df


# ----------------------------------------------------------------------------


def read_csv_columns_by_index(
    file_name: str,
    headers: dict[int, type],
    col_names: list[str],
    skip: int = 0,
) -> pd.DataFrame:
    """
    :param file_name: The file name to include path-link
    :param headers: A dictionary of column index and their data types.
                    types are limited to ``numpy.int64``, ``numpy.float64``,
                    and ``str``
    :param col_names: A list containing the names to be given to
                      each column
    :param skip: The number of lines to be skipped before reading data
    :return df: A pandas dataframe containing all relevant information
    :raises FileNotFoundError: If the file is found to not exist

    This function assumes the file has a comma (i.e. ,) delimiter, if
    it does not, then it is not a true .csv file and should be transformed
    to a text function and read by the xx function.  Assume we have a .csv
    file titled ``test.csv`` with the following format.

    .. list-table:: test.csv
      :widths: 6 10 6 6
      :header-rows: 0

      * - 1,
        - Shoes,
        - 1.5,
        - 5
      * - 2,
        - t-shirt,
        - 1.8,
        - 3,
      * - 3,
        - coffee,
        - 2.1,
        - 15
      * - 4,
        - books,
        - 3.2,
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_csv_columns_by_index

       > file_name = 'test.csv'
       > headers = {0: int, 1: str, 2: float, 3: int}
       > names = ['ID', 'Inventory', 'Weight_per', 'Number']
       > df = read_csv_columns_by_index(file_name, headers, names)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40

    This function can also use the `skip` attributed read data when the
    headers are not on the first line.  For instance, assume the following csv file;

    .. list-table:: test1.csv
      :widths: 16 8 5 5
      :header-rows: 0

      * - This line is used to provide metadata for the csv file
        -
        -
        -
      * - This line is as well
        -
        -
        -
      * - 1,
        - Shoes,
        - 1.5,
        - 5
      * - 2,
        - t-shirt,
        - 1.8,
        - 3,
      * - 3,
        - coffee,
        - 2.1,
        - 15
      * - 4,
        - books,
        - 3.2,
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_csv_columns_by_index

       > file_name = 'test1.csv'
        > headers = {0: int, 1: str, 2: float, 3: int}
       > names = ['ID', 'Inventory', 'Weight_per', 'Number']
       > df = read_csv_columns_by_index(file_name, headers,
                                        names, skip=2)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found")
    col_index = list(headers.keys())
    df = pd.read_csv(
        file_name, usecols=col_index, names=col_names, dtype=headers, skiprows=skip
    )
    return df


# ------------------------------------------------------------------------------------------


def read_text_columns_by_headers(
    file_name: str,
    headers: dict[str, type],
    skip: int = 0,
    delimiter=r"\s+",
) -> pd.DataFrame:
    """

    :param file_name: The file name to include path-link
    :param headers: A dictionary of column names and their data types.
                    types are limited to ``numpy.int64``, ``numpy.float64``,
                    and ``str``
    :param skip: The number of lines to be skipped before reading data
    :param delimiter: The type of delimiter separating data in the text file.
                Defaulted to space delimited, where a space is one or
                more white spaces.  This function can use any delimiter,
                to include a comma separation; however, a comma delimiter
                should be a .csv file extension.
    :return df: A pandas dataframe containing all relevant information
    :raises FileNotFoundError: If the file is found to not exist

    This function assumes the file has a space delimiter, if
    Assume we have a .csv file titled ``test.txt`` with the following
    format.

    .. list-table:: test.txt
      :widths: 6 10 6 6
      :header-rows: 1

      * - ID
        - Inventory
        - Weight_per
        - Number
      * - 1
        - Shoes
        - 1.5
        - 5
      * - 2
        - t-shirt
        - 1.8
        - 3
      * - 3
        - coffee
        - 2.1
        - 15
      * - 4
        - books
        - 3.2
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_text_columns_by_headers

       > file_name = 'test.txt'
       > headers = {'ID': int, 'Inventory': str, 'Weight_per': float, 'Number': int}
       > df = read_text_columns_by_headers(file_name, headers)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40

    This function can also use the `skip` attributed read data when the
    headers are not on the first line.  For instance, assume the following csv file;

    .. list-table:: test.txt
      :widths: 16 8 5 5
      :header-rows: 0

      * - This line is used to provide metadata for the csv file
        -
        -
        -
      * - This line is as well
        -
        -
        -
      * - ID
        - Inventory
        - Weight_per
        - Number
      * - 1
        - Shoes
        - 1.5
        - 5
      * - 2
        - t-shirt
        - 1.8
        - 3
      * - 3
        - coffee
        - 2.1
        - 15
      * - 4
        - books
        - 3.2
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_text_columns_by_headers

       > file_name = 'test.txt'
       > headers = {'ID': int, 'Inventory': str, 'Weight_per': float, 'Number': int}
       > df = read_text_columns_by_headers(file_name, headers, skip=2)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found")
    head = list(headers.keys())
    df = pd.read_csv(file_name, usecols=head, dtype=headers, skiprows=skip, sep=delimiter)
    return df


# --------------------------------------------------------------------------------


def read_text_columns_by_index(
    file_name: str,
    headers: dict[int, type],
    col_names: list[str],
    skip: int = 0,
    delimiter=r"\s+",
) -> pd.DataFrame:
    """

    :param file_name: The file name to include path-link
    :param headers: A dictionary of column index` and their data types.
                    types are limited to ``numpy.int64``, ``numpy.float64``,
                    and ``str``
    :param col_names: A list containing the names to be given to
                      each column
    :param skip: The number of lines to be skipped before reading data
    :param delimiter: The type of delimiter separating data in the text file.
                Defaulted to space delimited, where a space is one or
                more white spaces.  This function can use any delimiter,
                to include a comma separation; however, a comma delimiter
                should be a .csv file extension.
    :return df: A pandas dataframe containing all relevant information
    :raises FileNotFoundError: If the file is found to not exist

    Assume we have a .txt file titled ``test.txt`` with the following format.

    .. list-table:: test.txt
      :widths: 6 10 6 6
      :header-rows: 0

      * - 1
        - Shoes
        - 1.5
        - 5
      * - 2
        - t-shirt
        - 1.8
        - 3
      * - 3
        - coffee
        - 2.1
        - 15
      * - 4
        - books
        - 3.2
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_text_columns_by_index

       > file_name = 'test.txt'
       > headers = {0: int, 1: str, 2: float, 3: int}
       > names = [ headers = {'ID', 'Inventory', 'Weight_per', 'Number']
       > df = read_text_columns_by_index(file_name, headers, names)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40

    This function can also use the `skip` attributed read data when the
    headers are not on the first line.  For instance, assume the following csv file;

    .. list-table:: test.txt
      :widths: 16 8 5 5
      :header-rows: 0

      * - This line is used to provide metadata for the csv file
        -
        -
        -
      * - This line is as well
        -
        -
        -
      * - ID
        - Inventory
        - Weight_per
        - Number
      * - 1
        - Shoes
        - 1.5
        - 5
      * - 2
        - t-shirt
        - 1.8
        - 3
      * - 3
        - coffee
        - 2.1
        - 15
      * - 4
        - books
        - 3.2
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_text_columns_by_index

       > file_name = 'test.txt'
       > headers = {0: int, 1: str, 2: float, 3: int}
       > names = ['ID', 'Inventory', 'Weight_per', 'Number']
       > df = read_text_columns_by_index(file_name, headers,
                                         names, skip=2)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40

    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found")
    head = list(headers.keys())
    df = pd.read_csv(
        file_name,
        usecols=head,
        names=col_names,
        dtype=headers,
        skiprows=skip,
        sep=delimiter,
    )
    return df


# ------------------------------------------------------------------------------------------


def read_excel_columns_by_headers(
    file_name: str, tab: str, headers: dict[str, type], skip: int = 0
) -> pd.DataFrame:
    """

    :param file_name: The file name to include path-link.  Must be an
                      .xls file format.  This code will **not** read .xlsx
    :param tab: The tab or sheet name that data will be read from
    :param headers: A dictionary of column names and their data types.
                    types are limited to ``numpy.int64``, ``numpy.float64``,
                    and ``str``
    :param skip: The number of lines to be skipped before reading data
    :return df: A pandas dataframe containing all relevant information
    :raises FileNotFoundError: If the file is found to not exist

    Assume we have a .xls file titled ``test.xls`` with the following format
    in a tab titled ``primary``.

    .. list-table:: test.xls
      :widths: 6 10 6 6
      :header-rows: 1

      * - ID
        - Inventory
        - Weight_per
        - Number
      * - 1
        - Shoes
        - 1.5
        - 5
      * - 2
        - t-shirt
        - 1.8
        - 3
      * - 3
        - coffee
        - 2.1
        - 15
      * - 4
        - books
        - 3.2
        - 48

    This file can be read via the following command

    .. code-block:: python

       > file_name = 'test.xls'
       > tab = "primary"
       > headers = {'ID': int, 'Inventory': str, 'Weight_per': float, 'Number': int}
       > df = read_excel_columns_by_headers(file_name, tab, headers)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40

    This function can also use the `skip` attributed read data when the
    headers are not on the first line.  For instance, assume the following csv file;

    .. list-table:: test.xls
      :widths: 16 8 5 5
      :header-rows: 0

      * - This line is used to provide metadata for the csv file
        -
        -
        -
      * - This line is as well
        -
        -
        -
      * - ID
        - Inventory
        - Weight_per
        - Number
      * - 1
        - Shoes
        - 1.5
        - 5
      * - 2
        - t-shirt
        - 1.8
        - 3
      * - 3
        - coffee
        - 2.1
        - 15
      * - 4
        - books
        - 3.2
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_excel_columns_by_headers

       > file_name = 'test.xls'
       > tab = "primary"
       > headers = ['ID': int, 'Inventory': str, 'Weight_per': float, 'Number': int]
       > df = read_excel_columns_by_headers(file_name, tab,
                                            headers, skip=2)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found")
    head = list(headers.keys())
    df = pd.read_excel(
        file_name,
        sheet_name=tab,
        usecols=head,
        dtype=headers,
        skiprows=skip,
        engine="openpyxl",
    )
    return df


# ----------------------------------------------------------------------------


def read_excel_columns_by_index(
    file_name: str,
    tab: str,
    col_index: dict[int, str],
    col_names: list[str],
    skip: int = 0,
) -> pd.DataFrame:
    """

    :param file_name: The file name to include path-link.  Must be an
                      .xls file format.  This code will **not** read .xlsx
    :param tab: The tab or sheet name that data will be read from
    :param col_index: A dictionary of column index` and their data types.
                     types are limited to ``numpy.int64``, ``numpy.float64``,
                     and ``str``
    :param col_names: A list containing the names to be given to
                      each column
    :param skip: The number of lines to be skipped before reading data
    :return df: A pandas dataframe containing all relevant information
    :raises FileNotFoundError: If the file is found to not exist

    Assume we have a .txt file titled ``test.xls`` with the following format.

    .. list-table:: test.xls
      :widths: 6 10 6 6
      :header-rows: 0

      * - 1
        - Shoes
        - 1.5
        - 5
      * - 2
        - t-shirt
        - 1.8
        - 3
      * - 3
        - coffee
        - 2.1
        - 15
      * - 4
        - books
        - 3.2
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_excel_columns_by_index

       > file_name = 'test.xls'
       > tab = 'primary'
       > headers = {0: int, 1: str, 2: float, 3: int}
       > names = ['ID', 'Inventory', 'Weight_per', 'Number']
       > df = read_excel_columns_by_index(file_name, tab, headers, names)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40

    This function can also use the `skip` attributed read data when the
    headers are not on the first line.  For instance, assume the following csv file;

    .. list-table:: test.xls
      :widths: 16 8 5 5
      :header-rows: 0

      * - This line is used to provide metadata for the csv file
        -
        -
        -
      * - This line is as well
        -
        -
        -
      * - ID
        - Inventory
        - Weight_per
        - Number
      * - 1
        - Shoes
        - 1.5
        - 5
      * - 2
        - t-shirt
        - 1.8
        - 3
      * - 3
        - coffee
        - 2.1
        - 15
      * - 4
        - books
        - 3.2
        - 48

    This file can be read via the following command

    .. code-block:: python

       from cobralib.io import read_excel_columns_by_index

       > file_name = 'test.xls'
       > tab = "primary"
       > headers = {0: int, 1: str, 2: float, 3: int}
       > names = ['ID', 'Inventory', 'Weight_per', 'Number']
       > df = read_excel_columns_by_index(file_name, tab, headers,
                                          names, skip=2)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found")
    head = list(col_index.keys())
    df = pd.read_excel(
        file_name,
        sheet_name=tab,
        usecols=head,
        names=col_names,
        dtype=col_index,
        skiprows=skip,
        header=None,
        engine="openpyxl",
    )
    return df


# ------------------------------------------------------------------------------------------


def read_pdf_columns_by_headers(
    file_name: str,
    headers: dict[str, type],
    table_idx: int = 0,
    page_num: int = 0,
    skip: int = 0,
) -> pd.DataFrame:
    """
    Read a table from a PDF document and save user-specified columns into a pandas
    DataFrame. This function will read a pdf table that spans multiple
    pages. **NOTE:** The pdf document must be a vectorized pdf document and not
    a scan of another document for this function to work.

    :param file_name: The file name to include the path-link to the PDF file.
    :param headers: A dictionary of column names and their data types.
                    Data types are limited to ``int``, ``float``, and ``str``.
    :param table_idx: Index of the table to extract from the page (default: 0).
    :param page_num: Page number from which to extract the table (default: 0).
    :param skip: The number of lines to be skipped before reading data
    :return df: A pandas DataFrame containing the specified columns from the table.
    :raises FileNotFoundError: If the PDF file is found to not exist.

    Example usage:

    .. code-block:: python

       from cobralib.io import read_pdf_columns_by_headers

       > file_name = 'test.pdf'
       > headers = {'ID': int, 'Inventory': str, 'Weight_per': float, 'Number': int}
       > df = read_pdf_columns_by_headers(file_name, headers, table_idx=0, page_num=1)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found")

    # Extract tables from the specified page of the PDF using pdfplumber
    with pdfplumber.open(file_name) as pdf:
        page = pdf.pages[page_num]
        table = page.extract_tables()

    if table_idx >= len(table):
        raise ValueError(f"Table index {table_idx} out of range.")

    # Convert the table to a pandas DataFrame
    df = pd.DataFrame(table[table_idx][1:], columns=table[table_idx][0])

    # Skip specified number of rows before reading the header
    df = df.iloc[skip:]

    # Filter out columns based on user-specified headers
    selected_columns = [column for column in headers.keys() if column in df.columns]
    df = df[selected_columns]

    # Rename the columns to match the user-specified headers
    df.columns = list(headers.keys())

    # Convert the columns to the specified data types
    for column, dtype in headers.items():
        df[column] = df[column].astype(dtype)

    return df


# ------------------------------------------------------------------------------------------


def read_pdf_columns_by_index(
    file_name: str,
    headers: dict[int, type],
    col_names: list[str],
    table_idx: int = 0,
    skip_rows: int = 0,
    page_num: int = 0,
) -> pd.DataFrame:
    """
    Read a table from a PDF document and save user-specified columns into a pandas
    DataFrame based on their column index. This function will read a pdf table that
    spans multiple pages. **NOTE:** The pdf document must be a vectorized pdf
    document and not a scan of another document for this function to work.

    :param file_name: The file name to include the path-link to the PDF file.
    :param headers: A dictionary of column index and their data types.
                    Data types are limited to ``int``, ``float``, and ``str``.
    :param col_names: A list containing the names to be given to each column.
    :param table_idx: Index of the table to extract from the page (default: 0).
    :param skip_rows: Number of rows to skip before reading the header row (default: 0).
    :param page_num: Page number from which to extract the table (default: 0).
    :return df: A pandas DataFrame containing the specified columns from the table.
    :raises FileNotFoundError: If the PDF file is found to not exist.

    Example usage:

    .. code-block:: python

       from cobralib.io import read_pdf_columns_by_index

       > file_name = 'test.pdf'
       > headers = {0: int, 1: str, 2: float, 3: int}
       > col_names = ['ID', 'Inventory', 'Weight_per', 'Number']  # Column names
       > df = read_pdf_columns_by_index(file_name, headers, col_names,
                                        table_idx=0, skip_rows=2, page_num=1)
       > print(df)
           ID Inventory Weight_per Number
        0  1  shoes     1.5        5
        1  2  t-shirt   1.8        3
        2  3  coffee    2.1        15
        3  4  books     3.2        40
    """
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File '{file_name}' not found")

    # Extract tables from the specified page of the PDF using pdfplumber
    with pdfplumber.open(file_name) as pdf:
        page = pdf.pages[page_num]
        table = page.extract_tables()

    if table_idx >= len(table):
        raise ValueError(f"Table index {table_idx} out of range.")

    # Convert the table to a pandas DataFrame
    df = pd.DataFrame(table[table_idx][1:], columns=table[table_idx][0])

    # Skip specified number of rows before reading the header
    df = df.iloc[skip_rows:]

    # Filter out columns based on user-specified column indices
    selected_columns = [
        col_idx for col_idx in headers.keys() if col_idx < len(df.columns)
    ]
    df = df.iloc[:, selected_columns]

    # Rename the columns with user-specified column names
    df.columns = col_names[: len(selected_columns)]

    dat_type = list(headers.values())
    name_dict = dict(zip(col_names, dat_type))
    # Convert the columns to the specified data types
    for column, dtype in name_dict.items():
        df[column] = df[column].astype(dtype)

    return df


# ==========================================================================================
# ==========================================================================================
# READ AND WRITE TO YAML


def read_yaml_file(file_path: str, safe: bool = False, **kwargs) -> list[Any]:
    """
    This function can be used to read in the contents of a single yaml file, or
    a yaml file with multiple documents.  In order to accomodate thea reading
    of several documents, the contents are returned as a list, with each
    index representing a different document.  **NOTE** Under the hood, this
    funtion is using the pyyaml library and has all of its attributes.

    :param file_name: The file name to be read including the path length
    :param print_lines: The number of lines to be printed to the screen if the
                        user prints an instance of the class. Defaulted to 50
    :raises FileNotFoundError: If the file does not exist

    Example file titled test_file.yaml

    .. literalinclude:: ../../../data/test/test_file.yaml
       :language: text

    .. code-block:: python

       from cobralib.io import read_yaml_file

       data = read_yaml_file('test_file.yaml', safe=True)
       print(data)
       >> [{'name': 'John Doe', 'age': 25, 'occupation': 'Developer', 'hobbies':
          ['Reading', 'Coding', 'Playing guitar']}, {'name': 'Alice Smith',
           'age': 30, 'occupation': 'Designer', 'hobbies':
           ['Painting', 'Traveling', 'Hiking']}]

    """

    try:
        with open(file_path) as file:
            if safe:
                documents = list(yaml.safe_load_all(file, **kwargs))
            else:
                documents = list(yaml.load_all(file, Loader=yaml.Loader, **kwargs))
        return [doc for sublist in documents for doc in sublist]
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")


# ------------------------------------------------------------------------------------------


def write_yaml_file(file_path: str, data: dict, append: bool = False) -> None:
    """
    Write or append data to a YAML file.

    :param file_path: The path of the YAML file
    :param data: The data to be written or appended as a dictionary
    :param append: True to append data to the file, False to overwrite
                   the file or create a new one (default: False)
    :raises FileNotFoundError: If the file does not exist in append mode

    .. code-block:: python

       from corbalib.io import write_yaml_file

       dict_file = {'sports' : ['soccer', 'football', 'basketball',
                    'cricket', 'hockey', 'table tennis']},
                    {'countries' : ['Pakistan', 'USA', 'India',
                    'China', 'Germany', 'France', 'Spain']}
       # Create new yaml file
       write_yaml_file('new_file.yaml', data, dict_file, append=False)

    This will create a file titled new_file.yaml with the following contents

    .. literalinclude:: ../../../data/test/output.yaml
       :language: text

    """
    mode = "a" if append else "w"

    if append and not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found.")

    try:
        with open(file_path, mode) as file:
            if append:
                file.write("---\n")  # Add YAML document separator
            yaml.safe_dump(data, file)
    except OSError as e:
        print(f"Error writing to file: {e}")


# ==========================================================================================
# ==========================================================================================


class Logger:
    """
    Custom logging class that writes messages to both console and log file.

    :param filename: The name of the file to write logs to.
    :param console_level: The minimum logging level for the console. Should be one
                          of: 'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR',
                          'CRITICAL'.
    :param file_level: The minimum logging level for the log file. Should be one of:
                       'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
    :param max_lines: The maximum number of lines in the log file. When exceeded,
                      the oldest entries are deleted.
    :raises ValueError: If `console_level` or `file_level` are not valid logging
                        levels.
    :raises IOError: If an I/O error occurs when opening the file.

    **Example usage:**

    .. code-block:: python

        # create logger with filename='my_log.log', console_level='INFO',
        # file_level='DEBUG', and max_lines=100

        logger = Logger('my_log.log', 'INFO', 'DEBUG', 100)

        # log a DEBUG message
        logger.log('DEBUG', 'This is a debug message')

        # log an INFO message
        logger.log('INFO', 'This is an info message')
    """

    def __init__(self, filename, console_level, file_level, max_lines):
        self.filename = filename
        self.max_lines = max_lines

        # Creating logger
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(logging.DEBUG)

        # Creating console handler and setting its level
        ch = logging.StreamHandler()
        ch.setLevel(self._str_to_log_level(console_level))

        # Creating file handler and setting its level
        fh = logging.handlers.RotatingFileHandler(filename, backupCount=1)
        fh.setLevel(self._str_to_log_level(file_level))

        # Creating formatter
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(fmt)

        # Setting formatter for ch and fh
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # Adding ch and fh to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    # ------------------------------------------------------------------------------------------

    def _str_to_log_level(self, level):
        """
        Convert string representation of logging level to corresponding
        logging module constants.

        :param level: The string representation of the logging level.
        :return: Corresponding logging level.
        """
        levels = {
            "NOTSET": logging.NOTSET,
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return levels.get(level, logging.NOTSET)

    # ------------------------------------------------------------------------------------------

    def log(self, level, msg):
        """
        Write a log entry.

        :param level: The level of the log entry. Should be one of: 'NOTSET',
                      'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
        :param msg: The message to be logged.
        :raises ValueError: If `level` is not a valid logging level.
        """
        self.logger.log(self._str_to_log_level(level), msg)
        self._trim_log_file()

    def _trim_log_file(self):
        """
        Trims the log file to the last `max_lines` entries.

        :raises IOError: If an I/O error occurs when trying to trim the file.
        """
        try:
            with open(self.filename, "r+") as f:
                lines = deque(f, self.max_lines)
                f.seek(0)
                f.writelines(lines)
                f.truncate()
        except OSError:
            self.logger.exception("Error while trimming log file")


# ==========================================================================================
# ==========================================================================================
# eof
