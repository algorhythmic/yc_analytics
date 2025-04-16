"""
visualization.py
Reusable functions for generating Plotly charts and stats tables for the YC Analytics Dashboard.
"""
import plotly.express as px
import pandas as pd
import re

# --- Utility ---
def batch_to_year(batch):
    match = re.match(r"[SWF](\d{2})", str(batch))
    if match:
        yy = int(match.group(1))
        return 2000 + yy if yy < 100 else None
    return None

def add_batch_year_col(df, batch_col='batch'):
    if batch_col in df.columns:
        df = df.copy()
        df['batch_year'] = df[batch_col].apply(batch_to_year)
    else:
        df['batch_year'] = None
    return df

# --- Visualization Functions ---
def companies_launched_per_year(df):
    """Returns Plotly bar chart for companies launched per year (x=batch_year)."""
    launches_per_year = df.dropna(subset=['batch_year']).groupby('batch_year').size().reset_index(name='Company Count')
    fig = px.bar(launches_per_year, x='batch_year', y='Company Count', title='Companies Launched Per Year', labels={'batch_year': 'Year'})
    return fig

def median_team_size_over_time(df, only_chart=False):
    """Returns Plotly line chart (and optionally stats table) for team size by batch_year (excludes team_size <= 0)."""
    df_team = df[(df['team_size'] > 0) & df['batch_year'].notnull()]
    size_by_year = df_team.groupby('batch_year')['team_size'].median().reset_index()
    fig = px.line(size_by_year, x='batch_year', y='team_size', title='Median Team Size of New Companies Over Time', labels={'batch_year': 'Year'})
    if only_chart:
        return fig
    # Stats table for 2006-2010
    stats = df_team.groupby('batch_year')['team_size'].agg(['min', 'max', 'median', 'count']).reset_index()
    stats_2006_2010 = stats[(stats['batch_year'] >= 2006) & (stats['batch_year'] <= 2010)]
    return fig, stats_2006_2010

def industry_trends_over_time(df, top_n=7):
    """Returns Plotly area chart for industry trends over time (batch_year)."""
    if 'industry' not in df.columns:
        return None
    top_industries = df['industry'].value_counts().nlargest(top_n).index
    industry_trend = df[df['industry'].isin(top_industries) & df['batch_year'].notnull()]
    industry_counts = industry_trend.groupby(['batch_year', 'industry']).size().reset_index(name='Company Count')
    fig = px.area(industry_counts, x='batch_year', y='Company Count', color='industry',
                  title='Industry Representation Over Time',
                  labels={'batch_year': 'Year', 'Company Count': 'Companies'})
    # Move legend to top left as overlay
    fig.update_layout(
        legend=dict(
            x=0.01,
            y=0.99,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.7)',
            bordercolor='black',
            borderwidth=1
        )
    )
    return fig

def batch_over_time(df, batch_col='batch'):
    """Returns Plotly stacked bar chart for company count by batch over time (batch_year)."""
    batch_year_counts = df.dropna(subset=['batch_year']).groupby(['batch_year', batch_col]).size().reset_index(name='Company Count')
    fig = px.bar(
        batch_year_counts,
        x='batch_year',
        y='Company Count',
        color=batch_col,
        title='Company Count by Batch Over Time (Stacked)',
        labels={'batch_year': 'Year', batch_col: 'Batch'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(
        marker_line_width=1.5,
        marker_line_color='black',
        width=0.8,
        text=batch_year_counts['Company Count'],
        textposition='outside',
        texttemplate='%{x}'
    )
    fig.update_layout(bargap=0.05, bargroupgap=0.1)
    return fig

def batch_and_team_size_overlay(df, batch_col='batch'):
    """Stacked bar for company count by batch, with median team size as a white line (right y-axis, value labeled at last point). Legend is removed."""
    import plotly.graph_objects as go
    batch_year_counts = df.dropna(subset=['batch_year']).groupby(['batch_year', batch_col]).size().reset_index(name='Company Count')
    team_size_by_year = df[(df['team_size'] > 0) & df['batch_year'].notnull()].groupby('batch_year')['team_size'].median().reset_index()

    fig = px.bar(
        batch_year_counts,
        x='batch_year',
        y='Company Count',
        color=batch_col,
        title='Company Count by Batch Over Time (Stacked) with Median Team Size',
        labels={'batch_year': 'Year', batch_col: 'Batch'},
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    # Remove legend
    fig.update_layout(
        yaxis2=dict(
            title='Median Team Size',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        showlegend=False
    )
    # Add overlay line
    if not team_size_by_year.empty:
        last_x = team_size_by_year['batch_year'].iloc[-1]
        last_y = team_size_by_year['team_size'].iloc[-1]
        fig.add_trace(
            go.Scatter(
                x=team_size_by_year['batch_year'],
                y=team_size_by_year['team_size'],
                mode='lines+markers+text',
                name='Median Team Size',
                line=dict(color='white', width=3, dash='dash'),
                marker=dict(symbol='circle', size=8, color='white', line=dict(width=2, color='black')),
                yaxis='y2',
                text=[None]*(len(team_size_by_year)-1) + [f"{int(last_y)}"],
                textposition='middle right'
            )
        )
    fig.update_traces(marker_line_width=1.5, marker_line_color='black', selector=dict(type='bar'))
    fig.update_layout(bargap=0.05, bargroupgap=0.1)
    return fig
