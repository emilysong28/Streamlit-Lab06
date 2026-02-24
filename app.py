import streamlit as st
import pandas as pd

# importing all the methods, making them avail for app.py
from src.data import load_data
from src.filters import render_filters, apply_filters
from src.charts import plot_response_hist, plot_borough_bar, count_borough_bar
from src.layouts import header_metrics, body_layout_tabs


# -----------------------------
# IMT 561 Streamlit Lab Starter
# -----------------------------
#
# This repo is intentionally incomplete.
# During the lab, the instructor fills in TODO blocks live.
# Students then extend the same app for the in-class activity + assignment.


def main() -> None:
    st.set_page_config(
        page_title="NYC 311 Mini Dashboard (Lab)",
        layout="wide",
    )

    st.title("NYC 311 Mini Dashboard")
    st.caption("Starter app for IMT 561 lab: layouts + filters + coordinated views.")

    # ✅ Data loading (cached)
    df = load_data("data/sample.csv")

    # -------------------------
    # TODO (DEMO): Add a quick 'data sanity' check
    # - show row count
    # - show first 5 rows (optional)
    st.subheader("Data Sanity Check")
    st.write(f"Total rows: {len(df)}")
    st.dataframe(df.head(5), use_container_width=True)

    # -------------------------
    # Filters (sidebar by default)
    # -------------------------
    # render_filters returns a dictionary of user selections
    selections = render_filters(df)

    # apply_filters returns a filtered dataframe based on selections
    df_f = apply_filters(df, selections) # df_f constantly changes based on user selections

    # -------------------------
    # TODO (DEMO): Explain Streamlit re-runs
    # - changing a widget reruns the script top-to-bottom
    # - df_f changes because selections changes
    # -------------------------

    # -------------------------
    # Header metrics
    # -------------------------
    # TODO (IN-CLASS): Replace placeholder metrics with real calculations
    header_metrics(df_f)

    st.divider()

    # -------------------------
    # Main body
    # -------------------------
    # Tabs layout by default (3 tabs)
    tab_choice = st.radio(
        "Choose a layout for the body (lab demo uses tabs; assignment can remix):",
        ["Tabs (3)", "Two Columns"],
        horizontal=True,
    )

    if tab_choice == "Tabs (3)":
        body_layout_tabs(df_f)
    else:
        # -------------------------
        # TODO (DEMO): Implement a 2-column layout
        # - left column: a chart
        # - right column: a table
        # -------------------------
        # HINT: st.columns(2)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Response Time Distribution")
            plot_response_hist(df_f)

        with col2:
            st.subheader("Filtered Rows")
            st.dataframe(df_f, use_container_width=True, height=420)


    # -------------------------
    # TODO (IN-CLASS): Add a footer with a short 'design note'
    # - 2–3 sentences: who is the audience + what questions can they answer?
    st.divider()
    st.caption(
        "This dashboard is intended for NYC service analysts to identify the various types of service requests and their response time patterns across boroughs. "
        "It serves to answer questions such as: "
        "1. How does response times differ between different boroughs? "
        "2. What are common complaint types? "
        "3. Which boroughs have the fastest and slowest response rates? "
    )
    # -------------------------


if __name__ == "__main__":
    main()
