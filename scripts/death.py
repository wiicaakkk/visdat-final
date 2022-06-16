import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, DateRangeSlider, HoverTool, sources
from bokeh.layouts import row, column, gridplot, WidgetBox
from bokeh.models.widgets import Tabs, Panel, CheckboxGroup, Select
from bokeh.palettes import Category20_16
from datetime import datetime

def script_death(cv19):
  def make_dataset(country, date_range):
    yr = date_range
    subset = cv19[cv19['location'] == country]
    subset = subset[(subset['date'] >= yr[0]) & (subset['date'] <= yr[1])]


    new_src = ColumnDataSource(subset)
    return new_src

  def make_plot(src, origin):
    p = figure(plot_width = 800, plot_height = 600,
               x_axis_label='Date', x_axis_type='datetime', y_axis_label='Cases', title=f'Daily New Deaths on {origin}')
    p.line('date', 'new_deaths', source=src, color='firebrick', line_width=1)

    hover = HoverTool(tooltips=[('Country', '@location'), ('New deaths', '@new_deaths'), ('Date', '@date{%Y-%m-%d}')], formatters={'@date' :'datetime'},  line_policy='next')
    p.add_tools(hover)
    return p
  
  def style(p):
    p.title.align = 'center'
    p.title.text_font_size = '20pt'


		# Axis titles
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.axis_label_text_font_style = 'bold'
    p.xgrid.grid_line_color = None

		# Tick labels
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.major_label_text_font_size = '12pt'
    p.ygrid.grid_line_alpha = 0.8
    p.ygrid.grid_line_dash = [6, 4]

    return p
  
  def update(attr, old, new):
    origin = origin_select.value
    renj = range_select.value_as_datetime
    renj = list(renj)
    new_src = make_dataset(origin, renj)
    src.data.update(new_src.data)
    p.title.text=f'Daily New Cases on {origin}'

  origins = list(set(cv19['location']))
  origins.sort()
  origin_select = Select(title='Country', value='Afghanistan', options = origins)
  origin_select.on_change('value', update)

  range_select = DateRangeSlider(start=datetime(2022, 1, 1), end=datetime(2022, 12, 31), value=(datetime(2022,1,1), datetime(2022,1,31)), title='Date')
  range_select.on_change('value', update)

  initial_range = range_select.value_as_datetime
  initial_range = list(initial_range)
  initial_origin = origin_select.value

  src = make_dataset(initial_origin, initial_range)
  p = make_plot(src, initial_origin)
  p = style(p)

  controls = WidgetBox(origin_select, range_select)
  layout = row(controls, p)

  tab = Panel(child=layout, title='Line Chart(New Deaths)')
  return tab