import pandas as pd
import numpy as np
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from scripts.case import script_case
from scripts.death import script_death

df = pd.read_csv('data/owid-covid-data.csv')
mask = (df['date'] >= '2022-01-01') & (df['date'] <= '2022-06-10')
df_use = df.loc[mask]
df_use = df_use.reset_index(drop=True)
df_use['date'] = pd.to_datetime(df_use['date'])

tab1 = script_death(df_use)
tab2 = script_case(df_use)

tabs = Tabs(tabs = [tab1, tab2])

curdoc().add_root(tab)
curdoc().title = "worldwide covid in 2022 "
show(curdoc)