import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load data
df_customers = pd.read_csv('../data/saas_customers.csv',
                           parse_dates=['signup_date', 'churn_date'])
df_monthly = pd.read_csv('../data/saas_monthly.csv')

# Initialize app
app = Dash(__name__)

# Color scheme
COLORS = {
    'background': '#0f1117',
    'card': '#1e2130',
    'text': '#ffffff',
    'blue': '#4c9be8',
    'green': '#2ecc71',
    'red': '#e74c3c',
    'purple': '#9b59b6'
}

# KPI calculations
latest_mrr = df_monthly['mrr'].iloc[-1]
total_customers = df_monthly['active_customers'].iloc[-1]
avg_churn = df_monthly['churn_rate'].mean()
mrr_growth = ((df_monthly['mrr'].iloc[-1] / df_monthly['mrr'].iloc[0]) - 1) * 100

# Layout
app.layout = html.Div(style={'backgroundColor': COLORS['background'],
                              'padding': '20px', 'fontFamily': 'Arial'},
children=[

    # Title
    html.H1('SaaS Business Performance Dashboard',
            style={'color': COLORS['text'], 'textAlign': 'center',
                   'marginBottom': '10px'}),
    html.P('Interactive analytics for subscription business metrics (2021–2026)',
           style={'color': '#888', 'textAlign': 'center', 'marginBottom': '30px'}),

    # KPI Cards Row
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'},
    children=[
        # MRR Card
        html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '10px',
                        'padding': '20px', 'flex': '1', 'borderLeft': f"4px solid {COLORS['blue']}"},
        children=[
            html.P('Latest MRR', style={'color': '#888', 'margin': '0'}),
            html.H2(f"${latest_mrr:,.0f}", style={'color': COLORS['blue'], 'margin': '5px 0'}),
            html.P('Monthly Recurring Revenue', style={'color': '#666', 'fontSize': '12px'})
        ]),
        # Customers Card
        html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '10px',
                        'padding': '20px', 'flex': '1', 'borderLeft': f"4px solid {COLORS['green']}"},
        children=[
            html.P('Active Customers', style={'color': '#888', 'margin': '0'}),
            html.H2(f"{total_customers:,}", style={'color': COLORS['green'], 'margin': '5px 0'}),
            html.P('Current active subscribers', style={'color': '#666', 'fontSize': '12px'})
        ]),
        # Churn Card
        html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '10px',
                        'padding': '20px', 'flex': '1', 'borderLeft': f"4px solid {COLORS['red']}"},
        children=[
            html.P('Avg Churn Rate', style={'color': '#888', 'margin': '0'}),
            html.H2(f"{avg_churn:.1f}%", style={'color': COLORS['red'], 'margin': '5px 0'}),
            html.P('Monthly average churn', style={'color': '#666', 'fontSize': '12px'})
        ]),
        # Growth Card
        html.Div(style={'backgroundColor': COLORS['card'], 'borderRadius': '10px',
                        'padding': '20px', 'flex': '1', 'borderLeft': f"4px solid {COLORS['purple']}"},
        children=[
            html.P('MRR Growth', style={'color': '#888', 'margin': '0'}),
            html.H2(f"{mrr_growth:.0f}%", style={'color': COLORS['purple'], 'margin': '5px 0'}),
            html.P('Total growth since launch', style={'color': '#666', 'fontSize': '12px'})
        ]),
    ]),

    # Dropdown filter
    html.Div(style={'marginBottom': '20px'}, children=[
        html.Label('Filter by Plan:', style={'color': COLORS['text'], 'marginRight': '10px'}),
        dcc.Dropdown(
            id='plan-filter',
            options=[{'label': 'All Plans', 'value': 'All'}] +
                    [{'label': p, 'value': p} for p in ['Basic', 'Professional', 'Enterprise']],
            value='All',
            style={'width': '200px', 'display': 'inline-block'}
        )
    ]),

    # Charts Row 1
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'},
    children=[
        html.Div(style={'flex': '1', 'backgroundColor': COLORS['card'],
                        'borderRadius': '10px', 'padding': '15px'},
                 children=[dcc.Graph(id='mrr-chart')]),
        html.Div(style={'flex': '1', 'backgroundColor': COLORS['card'],
                        'borderRadius': '10px', 'padding': '15px'},
                 children=[dcc.Graph(id='customers-chart')]),
    ]),

    # Charts Row 2
    html.Div(style={'display': 'flex', 'gap': '20px'},
    children=[
        html.Div(style={'flex': '1', 'backgroundColor': COLORS['card'],
                        'borderRadius': '10px', 'padding': '15px'},
                 children=[dcc.Graph(id='plan-chart')]),
        html.Div(style={'flex': '1', 'backgroundColor': COLORS['card'],
                        'borderRadius': '10px', 'padding': '15px'},
                 children=[dcc.Graph(id='region-chart')]),
    ]),
])

# Callbacks
@app.callback(
    [Output('mrr-chart', 'figure'),
     Output('customers-chart', 'figure'),
     Output('plan-chart', 'figure'),
     Output('region-chart', 'figure')],
    [Input('plan-filter', 'value')]
)
def update_charts(selected_plan):
    # Filter customers
    if selected_plan == 'All':
        filtered = df_customers
    else:
        filtered = df_customers[df_customers['plan'] == selected_plan]

    # MRR Chart
    mrr_fig = go.Figure()
    mrr_fig.add_trace(go.Scatter(
        x=df_monthly['month'], y=df_monthly['mrr'],
        fill='tozeroy', line=dict(color=COLORS['blue'], width=2),
        name='MRR'))
    mrr_fig.update_layout(title='Monthly Recurring Revenue',
                          paper_bgcolor=COLORS['card'],
                          plot_bgcolor=COLORS['card'],
                          font=dict(color=COLORS['text']),
                          margin=dict(t=40, b=40))

    # Customers Chart
    cust_fig = go.Figure()
    cust_fig.add_trace(go.Scatter(
        x=df_monthly['month'], y=df_monthly['active_customers'],
        fill='tozeroy', line=dict(color=COLORS['green'], width=2),
        name='Active Customers'))
    cust_fig.update_layout(title='Active Customers',
                           paper_bgcolor=COLORS['card'],
                           plot_bgcolor=COLORS['card'],
                           font=dict(color=COLORS['text']),
                           margin=dict(t=40, b=40))

    # Plan Revenue Chart
    plan_rev = filtered.groupby('plan')['monthly_price'].sum().reset_index()
    plan_fig = px.bar(plan_rev, x='plan', y='monthly_price',
                      color='plan',
                      color_discrete_map={'Basic': COLORS['blue'],
                                         'Professional': COLORS['green'],
                                         'Enterprise': COLORS['purple']},
                      title='Revenue by Plan Type')
    plan_fig.update_layout(paper_bgcolor=COLORS['card'],
                           plot_bgcolor=COLORS['card'],
                           font=dict(color=COLORS['text']),
                           margin=dict(t=40, b=40),
                           showlegend=False)

    # Region Chart
    region_rev = filtered.groupby('region')['monthly_price'].sum().reset_index()
    region_fig = px.bar(region_rev, x='monthly_price', y='region',
                        orientation='h', title='Revenue by Region',
                        color_discrete_sequence=[COLORS['blue']])
    region_fig.update_layout(paper_bgcolor=COLORS['card'],
                              plot_bgcolor=COLORS['card'],
                              font=dict(color=COLORS['text']),
                              margin=dict(t=40, b=40))

    return mrr_fig, cust_fig, plan_fig, region_fig

if __name__ == '__main__':
    app.run(debug=True)