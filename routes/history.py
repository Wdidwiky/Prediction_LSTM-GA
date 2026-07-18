from io import StringIO

from flask import Blueprint, Response, render_template, request

from utils.data_loader import load_history

history_bp = Blueprint("history", __name__)

PAGE_SIZE = 25
PRICE_COLUMNS = ("Open", "High", "Low", "Close")


def _prepare_history(df):
    """Normalize the Yahoo Finance data before it is displayed or downloaded."""
    df = df.copy()
    df["Date"] = df["Date"].astype("datetime64[ns]")
    return df.sort_values("Date", ascending=False).reset_index(drop=True)


@history_bp.route("/history")
def history():
    all_history = _prepare_history(load_history().reset_index())
    df = all_history
    query = request.args.get("q", "").strip()

    if query:
        date_text = df["Date"].dt.strftime("%Y-%m-%d")
        df = df[date_text.str.contains(query, case=False, na=False)]

    total_rows = len(df)
    total_pages = max(1, (total_rows + PAGE_SIZE - 1) // PAGE_SIZE)
    page = request.args.get("page", 1, type=int)
    page = min(max(page, 1), total_pages)
    start = (page - 1) * PAGE_SIZE

    display_df = df.iloc[start:start + PAGE_SIZE].copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
    for column in PRICE_COLUMNS:
        if column in display_df:
            display_df[column] = display_df[column].map(lambda value: f"${value:,.2f}")
    if "Volume" in display_df:
        display_df["Volume"] = display_df["Volume"].map(lambda value: f"{value:,.0f}")

    latest = all_history.iloc[0]
    return render_template(
        "history.html",
        columns=display_df.columns,
        rows=display_df.to_dict("records"),
        last_price=f"${latest['Close']:,.2f}",
        highest=f"${all_history['High'].max():,.2f}",
        lowest=f"${all_history['Low'].min():,.2f}",
        query=query,
        page=page,
        total_pages=total_pages,
        total_rows=total_rows,
    )


@history_bp.route("/history/download")
def download_history():
    df = _prepare_history(load_history())
    output = StringIO()
    df.to_csv(output, index=False, date_format="%Y-%m-%d")
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=brent_price_history.csv"},
    )
