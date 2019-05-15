import pandas as pd
import sqlite3
from urllib.parse import urlparse
from tld import get_tld, get_fld

# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("crawl-data-test.sqlite")

site_visits = pd.read_sql_query("SELECT * from site_visits", con)
javascript = pd.read_sql_query("SELECT * from javascript", con)

# verify that result of SQL query is stored in the dataframe
site_visits.head()
javascript.head()

con.close()