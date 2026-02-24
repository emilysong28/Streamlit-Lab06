import pandas as pd
import streamlit as st

from src.charts import plot_response_hist, plot_borough_bar, count_borough_bar


def header_metrics(df: pd.DataFrame) -> None:
    """Rendering header metrics. Placeholder values are intentional."""
    c1, c2, c3 = st.columns(3)

    # TODO (IN-CLASS): Replace these placeholders with real metrics from df
    # Suggestions:
    # - Total complaints (len(df))
    # - Median response time
    # - % from Web vs Phone vs App (pick one)
    total_complaints = len(df)
    median_response_days = round(df['response_time_days'].median(), 2)
    most_common_complaint = df['complaint_type'].value_counts().idxmax()

    with c1:
        st.metric("Total complaints", total_complaints)
    with c2:
        st.metric("Median response (days)", median_response_days)
    with c3:
        st.metric("Most common complaint", most_common_complaint)


def body_layout_tabs(df: pd.DataFrame) -> None:
    """Tabs layout with 3 default tabs."""
    t1, t2, t3 = st.tabs(["Distribution", "By Borough", "Table"])

    with t1:
        st.subheader("Response Time Distribution")
        plot_response_hist(df)

        # TODO (IN-CLASS): Add a short interpretation sentence under the chart
        median_response_time = df["response_time_days"].median()
        st.caption(
            f"Median response time is **{median_response_time:.1f} days**, "
            "indicating how quickly requests are typically resolved."
        )

    with t2:
        st.subheader("Median Response Time by Borough")
        plot_borough_bar(df)

        # TODO (IN-CLASS): Add a second view here (e.g., count by borough)
        # plot # of complaints for each borough
        st.subheader("Complaint Count by Borough")
        count_borough_bar(df)

    with t3:
        st.subheader("Filtered Rows")
        st.dataframe(df, use_container_width=True, height=480)

        # TODO (OPTIONAL): Add st.download_button to export filtered rows
