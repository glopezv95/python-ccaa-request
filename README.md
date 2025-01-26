# Spain's provinces and Autonomous Communities Standardiser
This project (`inereq.py`) includes the definition of a class, `CCAA`, that, when initialised, makes a GET request to the spanish [Statistic National Institute (INE)](https://ine.es/) to retrieve the standardised names of the provinces and Autonomous Communities of Spain, as well as their respective official identification codes.

The definition of this class includes a method, `CCAA().normalise_values`, that generates a standardised list of either provinces or Autonomous Communities from an input list by replacing its values with the ones retrieved from the [INE](https://ine.es/) using the [*rapidfuzz*](https://pypi.org/project/RapidFuzz/) library. The data obtained from the GET request gets stored in the class as a [`bs4.Beautifulsoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#bs4.BeautifulSoup) class, and the table both as a [`bs4.element.Tag`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#bs4.Tag) and a [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).

## Installation
### 1. Create and activate a virtual environment (*optional*)

#### cmd
```cmd
python -m venv [virtual_environment_name]
venv/scripts/activate
```

#### bash
```
python3 -m venv [virtual_environment_name]
source venv/bin/activate
```

### 2. Install dependencies
#### cmd/bash
```
pip install -r requirements.txt
```