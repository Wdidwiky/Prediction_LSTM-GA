from pathlib import Path

from flask import Blueprint, render_template
import pandas as pd
import plotly.graph_objects as go

from utils.metrics import calculate_metrics
from utils.predictor import predict

model_bp = Blueprint("model", __name__)

PROJECT_DIR = Path(__file__).resolve().parents[1]

BEST_HYPERPARAMETERS = (
    ("Unit LSTM", "128"),
    ("Dropout", "0.15"),
    ("Laju pembelajaran", "0.001"),
    ("Ukuran batch", "16"),
    ("Maksimum epoch", "100"),
)

GA_CONFIGURATION = (
    ("Populasi", "20 individu"),
    ("Generasi", "20"),
    ("Crossover", "Two-point · 0.50"),
    ("Mutasi", "Custom mutation · 0.30"),
    ("Seleksi", "Tournament · ukuran 3"),
    ("Fitness", "Validation RMSE (minimum)"),
)

HYPERPARAMETER_ROWS = (
    {
        "label": "Unit LSTM",
        "best": "128",
        "candidates": (32, 64, 128, 256),
    },
    {
        "label": "Dropout",
        "best": "0.15",
        "candidates": (0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5),
    },
    {
        "label": "Learning rate",
        "best": "0.001",
        "candidates": (0.001, 0.0005, 0.0001),
    },
    {
        "label": "Batch size",
        "best": "16",
        "candidates": (16, 32, 64),
    },
    {
        "label": "Epochs",
        "best": "100",
        "candidates": (50, 100, 150),
    },
)

ARCHITECTURE = (
    ("LSTM", "128 Units (return_sequences=True)", "(60,128)", "66,560"),
    ("Dropout", "Rate 0.15", "(60,128)", "0"),
    ("LSTM", "128 Units", "(128)", "131,584"),
    ("Dropout", "Rate 0.15", "(128)", "0"),
    ("Dense", "1 Output Neuron", "(1)", "129"),
)

# Best validation loss recorded at epoch 77 in the final training run.
TRAINING_VALIDATION_LOSS = 0.00028970


def _build_dataset_split_chart(prediction_df):
    train_size = int(len(prediction_df) * 0.70)
    val_size = int(len(prediction_df) * 0.15)

    train_df = prediction_df.iloc[:train_size]
    val_df = prediction_df.iloc[train_size:train_size + val_size]
    test_df = prediction_df.iloc[train_size + val_size:]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=prediction_df["Date"],
            y=prediction_df["Close"],
            mode="lines",
            name="Actual",
            line=dict(color="#111827", width=1.5),
            opacity=0.35,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=train_df["Date"],
            y=train_df["Close"],
            mode="lines",
            name="Training",
            line=dict(color="#2563eb", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=val_df["Date"],
            y=val_df["Close"],
            mode="lines",
            name="Validation",
            line=dict(color="#f59e0b", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=test_df["Date"],
            y=test_df["Close"],
            mode="lines",
            name="Testing",
            line=dict(color="#16a34a", width=2),
        )
    )
    fig.update_layout(
        template="plotly_white",
        title="Actual Data dan Pembagian Training, Validation, Testing",
        xaxis_title="Tanggal",
        yaxis_title="Harga Brent Crude Oil",
        legend_title="Dataset",
        hovermode="x unified",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig.to_html(full_html=False)


@model_bp.route("/model")
def model():
    logbook = pd.read_csv(PROJECT_DIR / "GA_Logbook.csv")
    prediction_df = predict()
    metrics = calculate_metrics(prediction_df["Close"], prediction_df["Prediction"])
    metrics["validation_loss"] = TRAINING_VALIDATION_LOSS
    dataset_split_graph = _build_dataset_split_chart(prediction_df)
    curve = go.Figure()
    curve.add_trace(
        go.Scatter(
            x=logbook["gen"], y=logbook["min"], mode="lines+markers",
            name="Best RMSE", line={"color": "#2563eb", "width": 3},
        )
    )
    curve.add_trace(
        go.Scatter(
            x=logbook["gen"], y=logbook["avg"], mode="lines+markers",
            name="Average RMSE", line={"color": "#94a3b8", "width": 2, "dash": "dot"},
        )
    )
    curve.update_layout(
        template="plotly_white",
        margin={"l": 16, "r": 16, "t": 20, "b": 16},
        hovermode="x unified",
        legend={"orientation": "h", "y": 1.12, "x": 0},
        xaxis={"title": "Generation", "dtick": 1, "showgrid": False},
        yaxis={"title": "RMSE", "gridcolor": "#e5e7eb"},
    )
    return render_template(
        "model.html",
        metrics=metrics,
        evaluation_date=pd.to_datetime(prediction_df["Date"]).max().strftime("%d-%m-%Y"),
        hyperparameters=BEST_HYPERPARAMETERS,
        ga_configuration=GA_CONFIGURATION,
        hyperparameter_rows=HYPERPARAMETER_ROWS,
        architecture=ARCHITECTURE,
        generations=int(logbook["gen"].max()),
        best_ga_rmse=float(logbook["min"].min()),
        dataset_split_graph=dataset_split_graph,
        learning_curve=curve.to_html(
            full_html=False, config={"responsive": True, "displaylogo": False}
        ),
    )
