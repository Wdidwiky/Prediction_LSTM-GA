from io import StringIO

from flask import Blueprint, Response, render_template
import plotly.graph_objects as go

from utils.forecast import forecast_next_days

forecast_bp = Blueprint("forecast", __name__)


def _get_forecast():
    """Generate the forecast once and retain the most recent actual price."""
    return forecast_next_days()


@forecast_bp.route("/forecast")
def forecast():
    df = _get_forecast()

    fig = go.Figure(
        go.Scatter(
            x=df["Date"],
            y=df["Forecast"],
            mode="lines+markers",
            name="Forecast",
            line={"color": "#2563eb", "width": 3},
            marker={"size": 7, "color": "#1d4ed8"},
            hovertemplate="%{x|%d %b %Y}<br>Forecast: $%{y:,.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_white",
        margin={"l": 16, "r": 16, "t": 20, "b": 16},
        hovermode="x unified",
        xaxis={"title": None, "showgrid": False},
        yaxis={"title": "Price (USD)", "tickprefix": "$", "gridcolor": "#e5e7eb"},
        showlegend=False,
    )

    table_df = df.copy()
    table_df["Date"] = table_df["Date"].dt.strftime("%d %b %Y")
    table_df["Forecast"] = table_df["Forecast"].map(lambda value: f"${value:,.2f}")
    return render_template(
        "forecast.html",
        graph=fig.to_html(full_html=False, config={"responsive": True, "displaylogo": False}),
        columns=table_df.columns,
        rows=table_df.to_dict("records"),
        last_price=f"${df.attrs['last_price']:,.2f}",
        average_forecast=f"${df['Forecast'].mean():,.2f}",
        highest_forecast=f"${df['Forecast'].max():,.2f}",
        lowest_forecast=f"${df['Forecast'].min():,.2f}",
        total_days=len(df),
    )


@forecast_bp.route("/forecast/download")
def download_forecast():
    df = _get_forecast()
    output = StringIO()
    df.to_csv(output, index=False, date_format="%Y-%m-%d")
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=brent_forecast_14_days.csv"},
    )
