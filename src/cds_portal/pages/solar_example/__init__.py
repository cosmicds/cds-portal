
import solara
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Function to convert decimal year to datetime
def decimal_year_to_date(decimal_year):
    year = int(decimal_year)
    rem = decimal_year - year
    base = datetime(year, 1, 1)
    next_year = datetime(year + 1, 1, 1)
    return base + (next_year - base) * rem

# Load data
from pathlib import Path
current_dir = Path(__file__).parent
sunspot_df = pd.read_csv(current_dir / "sunspot_data_1945_2018.csv")
tsi_df = pd.read_csv(current_dir / "tsi_data_1945_2018.csv")

# Convert decimal years to datetime
sunspot_df['Date'] = sunspot_df['Year'].apply(decimal_year_to_date)
tsi_df['Date'] = tsi_df['Year'].apply(decimal_year_to_date)

# Solar cycle start dates and labels (Cycle 18 to 24)
solar_cycle_starts = [1944.2, 1954.3, 1964.9, 1976.5, 1986.8, 1996.4, 2008.9]
solar_cycle_labels = [f"Cycle {n}" for n in range(18, 25)]
solar_cycle_dates = pd.Series(solar_cycle_starts).apply(decimal_year_to_date)

@solara.component
def Page():
    fig = go.Figure()

    # Sunspot trace
    fig.add_trace(go.Scatter(
        x=sunspot_df['Date'], y=sunspot_df['Sunspot_Number'],
        name='Sunspot Number', yaxis='y1', line=dict(color='darkblue'),
        hovertemplate='Date: %{x|%Y-%m-%d}<br>Sunspots: %{y:.0f}'
    ))

    # TSI trace
    fig.add_trace(go.Scatter(
        x=tsi_df['Date'], y=tsi_df['TSI'],
        name='TSI (W/m^2)', yaxis='y2',
        line=dict(color='darkorange', width=3),
        hovertemplate='Date: %{x|%Y-%m-%d}<br>TSI: %{y:.2f}'
    ))

    # Add solar cycle lines and annotations
    for date, label in zip(solar_cycle_dates, solar_cycle_labels):
        fig.add_shape(
            type='line',
            x0=date, x1=date, y0=0, y1=1,
            xref='x', yref='paper',
            line=dict(color='dimgray', dash='dot', width=1)
        )
        fig.add_annotation(
            x=date, y=1.05, xref='x', yref='paper',
            text=label,
            showarrow=False,
            font=dict(size=10, color='dimgray')
        )

    # Layout settings
    fig.update_layout(
        title="Sunspot Number (daily) and TSI (yearly), 1945–2018",
        xaxis=dict(
            title="Date",
            showline=True,
            linewidth=1,
            linecolor='black',
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            griddash='dot'
        ),
        yaxis=dict(
            title="Sunspot Number",
            titlefont=dict(color='darkblue'),
            tickfont=dict(color='darkblue'),
            side="left",
            showgrid=True,
            gridcolor="blue",
            griddash='dot',
            tickformat=".0f",
            nticks=6
        ),
        yaxis2=dict(
            title=dict(
                text="TSI (W/m^2)",
                font=dict(color='darkorange'),
                standoff=10
            ),
            tickfont=dict(color='darkorange'),
            overlaying="y",
            side="right",
            showgrid=True,
            gridcolor="orange",
            griddash='dot',
            tickformat=".2f",
            nticks=6
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(x=1.02, y=1, xanchor='left', yanchor='top'),
        hovermode="x unified",
        height=500
    )

    solara.FigurePlotly(fig)
