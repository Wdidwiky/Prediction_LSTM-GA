from flask import Blueprint, render_template
from utils.predictor import predict
from utils.forecast import forecast_next_days
from utils.metrics import calculate_metrics

import plotly.graph_objects as go

dashboard_bp = Blueprint("dashboard", __name__)


def _build_actual_prediction_chart(prediction_df):
    chart_df = prediction_df.copy()
    chart_df["Close"] = chart_df["Close"].round(2)
    chart_df["Prediction"] = chart_df["Prediction"].round(2)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=chart_df["Date"],
            y=chart_df["Close"],
            mode="lines",
            name="Actual",
            line=dict(color="#111827", width=2)
        )
    )
    fig.add_trace(
        go.Scatter(
            x=chart_df["Date"],
            y=chart_df["Prediction"],
            mode="lines",
            name="Prediction",
            line=dict(color="#ef4444", width=2, dash="dash")
        )
    )
    fig.update_layout(
        template="plotly_white",
        title="Actual vs Prediction",
        xaxis_title="Tanggal",
        yaxis_title="Harga Brent Crude Oil",
        legend_title="Data",
        hovermode="x unified",
        margin=dict(l=40, r=20, t=60, b=40)
    )
    return fig.to_html(full_html=False)


@dashboard_bp.route("/")
def dashboard():
    prediction_df = predict()
    forecast_df = forecast_next_days()

    current_price = round(prediction_df["Close"].iloc[-1],2)
    metrics = calculate_metrics(prediction_df["Close"], prediction_df["Prediction"])

    forecast_fig = go.Figure()

    forecast_fig.add_trace(
        go.Scatter(
            x=forecast_df["Date"],
            y=forecast_df["Forecast"],
            mode="lines+markers",
            name="Forecast"
        )
    )
    forecast_fig.update_layout(
        template="plotly_white",
        title="Forecast Brent Price (14 Days)"
    )
    forecast_graph = forecast_fig.to_html(full_html=False)

    actual_prediction_graph = _build_actual_prediction_chart(prediction_df)

    return render_template(
        "dashboard.html",
        actual_prediction_graph=actual_prediction_graph,
        forecast_graph=forecast_graph,
        forecast_table=forecast_df.to_html(
            classes="table table-striped table-hover", index=False
        ),
        current_price=f"${current_price:,.2f}",
        metrics=metrics
    )
