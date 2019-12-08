import dash
import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt, date

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
  html.H2('Dates'),
  dcc.DatePickerRange(
      id='ticker-range',
      display_format='MMM Do, YY',
      # updatemode='bothdates',
      initial_visible_month=date.today(),
      end_date=date.today()
  ),
  html.H2('Interval'),
  dcc.Dropdown(
    id='ticker-interval',
    # 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    options=[
      {'label': '1 minute',   'value': '1m'},
      {'label': '2 minutes',  'value': '2m'},
      {'label': '5 minutes',  'value': '5m'},
      {'label': '15 minutes', 'value': '15m'},
      {'label': '30 minutes', 'value': '30m'},
      {'label': '60 minutes', 'value': '60m'},
      {'label': '90 minutes', 'value': '90m'},
      {'label': '1 hour',     'value': '1h'},
      {'label': '1 day',      'value': '1d'},
      {'label': '5 days',     'value': '5d'},
      {'label': '1 week',     'value': '1wk'},
      {'label': '1 month',    'value': '1mo'},
      {'label': '3 months',   'value': '3mo'},
    ],
    value='15m'
  ),
  html.H2('Ticker'),
  dcc.Input(
    id="ticker-search",
    type="search",
    debounce=True,
    placeholder="search for stock",
    className="mb-3"
  ),
  html.Div(id="ticker-out"),
  html.Div(id='output-container-date-picker-range')
])

@app.callback(
    dash.dependencies.Output("ticker-out", "children"),
    [dash.dependencies.Input("ticker-search", "value")],
)
def ticker_render(ticker):
  return "Ticker: {}".format(ticker)

@app.callback(
  dash.dependencies.Output('output-container-date-picker-range', 'children'),
  [dash.dependencies.Input('ticker-range', 'start_date'),
    dash.dependencies.Input('ticker-range', 'end_date')
  ])
def update_output(start_date, end_date):
  string_prefix = 'You have selected: '
  if start_date is not None:
    start_date = dt.strptime(start_date.split(' ')[0], '%Y-%m-%d')
    start_date_string = start_date.strftime('%B %d, %Y')
    string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
  if end_date is not None:
    end_date = dt.strptime(end_date.split(' ')[0], '%Y-%m-%d')
    end_date_string = end_date.strftime('%B %d, %Y')
    string_prefix = string_prefix + 'End Date: ' + end_date_string
  if len(string_prefix) == len('You have selected: '):
    return 'Select a date to see it displayed here'
  else:
    return string_prefix

if __name__ == '__main__':
  app.run_server(debug=True)
