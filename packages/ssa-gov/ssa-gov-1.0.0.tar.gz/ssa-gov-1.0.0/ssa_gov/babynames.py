from datetime import datetime
from typing import Dict, Tuple, List, Union, Optional

import pandas as pd
from bs4 import BeautifulSoup, Tag
from pandas import DataFrame
from requests import Response, Session

from ssa_gov.utilities import create_session


def get_popular_baby_names(
        year: int,
        n: int,
        session: Optional[Session] = None
) -> Tuple[DataFrame, DataFrame]:
    """
    Retrieves popular names data for a given year and number of names.

    Args:
        year (int): The year for which data is to be retrieved.
        n (int): The number of names to retrieve.
        session (Optional[Session], optional): The session to use for the request. Defaults to None.

    Returns:
        Tuple[DataFrame, DataFrame]: A tuple of DataFrames containing male and female popular names.
    """
    # If the user has not provided a session, create one with a random User-Agent
    if session is None:
        session = create_session()

    # Validate the input year and n
    current_year: int = datetime.now().year
    if not (1880 <= year < current_year):
        raise ValueError(f"Year must be between 1880 and {current_year - 1}")
    if not (1 <= n <= 1000):
        raise ValueError("n must be between 1 and 1000")

    # Set up data for the POST request
    data: Dict[str, Union[int, str]] = {
        'year': year,
        'top': n,
        'number': 'n',
        'token': 'Submit',
    }

    # Perform the post request
    response: Response = session.post('https://www.ssa.gov/cgi-bin/popularnames.cgi', data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the response content using BeautifulSoup
    soup: BeautifulSoup = BeautifulSoup(response.content, 'html5lib')

    # Find the table with the specified summary
    table: Optional[Tag] = soup.find('table', summary=f"Popularity for top {n}")
    if not table:
        raise ValueError(f"Table with summary 'Popularity for top {n}' not found in the response.")

    # Load the table data into a DataFrame and use the first column as the index
    df: DataFrame = pd.read_html(table.prettify(), header=0, index_col=0, flavor='html5lib')[0]

    # Exclude the last row
    df = df.iloc[:-1]

    # Splitting the dataframe into male and female dataframes
    male_df: DataFrame = df.iloc[:, 0:2]
    female_df: DataFrame = df.iloc[:, 2:4]

    # Renaming columns for each dataframe
    male_df.columns = ["Name", "Count"]
    female_df.columns = ["Name", "Count"]

    return male_df, female_df


def get_baby_name_popularity_data(
        name: str,
        since_year: int,
        sex: str,
        session: Optional[Session] = None
) -> Optional[DataFrame]:
    """
    Retrieves popularity data for a given name since a specified year.

    Args:
        name (str): The name for which data is to be retrieved.
        since_year (int): The starting year for the data.
        sex (str): Gender (either 'M' or 'F').
        session (Optional[Session], optional): The session to use for the request. Defaults to None.

    Returns:
        Optional[DataFrame]: A DataFrame containing the name popularity data, or None if no data is found.
    """
    # If the user has not provided a session, create one with a random User-Agent
    if session is None:
        session = create_session()

    # Input validation
    current_year: int = datetime.now().year
    if not (1880 <= since_year < current_year):
        raise ValueError(f"since_year must be between 1880 and {current_year - 1}")
    if sex not in ['M', 'F']:
        raise ValueError("sex must be either 'M' or 'F'")
    if len(name) < 2:
        raise ValueError("Name must be at least 2 characters long")

    # Set up data for the POST request
    data: Dict[str, Union[str, int]] = {
        'name': name,
        'start': since_year,
        'sex': sex,
        'token': 'Submit'
    }

    # Perform the POST request
    response: Response = session.post('https://www.ssa.gov/cgi-bin/babyname.cgi', data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the response using BeautifulSoup
    soup: BeautifulSoup = BeautifulSoup(response.content, 'html5lib')

    # Check for a h3 tag indicating missing data
    h3_tag: Optional[Tag] = soup.find('h3')

    # If there is no data to be extracted, return None
    if h3_tag:
        return None

    # Locate the <blockquote> tag
    blockquote: Optional[Tag] = soup.find('blockquote')

    if not blockquote:
        raise ValueError("Blockquote element not found in the response.")

    # Find the next <p> tag after the blockquote
    p_tag: Optional[Tag] = blockquote.find_next('p')

    if not p_tag:
        raise ValueError("P element not found after the blockquote.")

    # Extract data from <tr> elements under the <p> tag
    data: List[Tuple[str, str]] = []
    for tr in p_tag.find_all('tr') if p_tag else []:
        tds: List[Tag] = tr.find_all('td')
        if len(tds) >= 2:  # Ensure we have at least two <td> elements
            data.append((tds[0].get_text(strip=True), tds[1].get_text(strip=True)))

    # Load data into a DataFrame
    df: DataFrame = DataFrame(data, columns=['Year', 'Count'])

    return df


if __name__ == '__main__':
    print(get_popular_baby_names(2020, 1000))
    print(get_baby_name_popularity_data("Meryl", 1880, 'F'))
