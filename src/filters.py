import pandas as pd
import streamlit as st

# change the type
def render_filters(df: pd.DataFrame) -> dict:
    """Rendering filter widgets and returning the chosen values."""
    st.sidebar.header("Filters")

    boroughs = ["All"] + sorted(df["borough"].unique().tolist())
    channels = ["All"] + sorted(df["channel"].unique().tolist())
    complaint_types = sorted(df["complaint_type"].unique().tolist())

    borough = st.sidebar.selectbox("Borough", boroughs, index=0)
    channel = st.sidebar.selectbox("Channel", channels, index=0)

    # TODO (DEMO): Convert this selectbox to a multiselect (and update filtering logic)
    complaint = st.sidebar.multiselect("Complaint Type", complaint_types, default=complaint_types)

    # Response time slider
    min_rt, max_rt = float(df["response_time_days"].min()), float(df["response_time_days"].max())
    rt_range = st.sidebar.slider(
        "Response time (days)",
        min_value=0.0,
        max_value=float(max_rt),
        value=(0.0, float(min(30.0, max_rt))),
        step=0.5,
    )

    # TODO (IN-CLASS): Add a checkbox toggle to cap outliers (e.g., at 99th percentile)
    cap_outliers = st.sidebar.checkbox("Cap extreme response times", value=False)

    return {
        "borough": borough,
        "channel": channel,
        "complaint": complaint,
        "rt_range": rt_range,
        "cap_outliers": cap_outliers,
    }


def apply_filters(df: pd.DataFrame, selections: dict) -> pd.DataFrame:
    """Applying filter selections to the dataframe."""
    out = df.copy()

    if selections["borough"] != "All":
        out = out[out["borough"] == selections["borough"]]

    if selections["channel"] != "All":
        out = out[out["channel"] == selections["channel"]]

    complaints = selections.get("complaint", []) # empty list
    if complaints:
        out = out[out["complaint_type"].isin(complaints)] # change complain selection to a list of items

    lo, hi = selections["rt_range"]
    out = out[(out["response_time_days"] >= lo) & (out["response_time_days"] <= hi)]

    # TODO (IN-CLASS): Implement outlier capping when cap_outliers is checked
    # HINT: use out["response_time_days"].quantile(0.99) # change this
    # if checkbox is checked and dataframe is not empty
    if selections.get("cap_outliers", False) and not out.empty: # look for cap_outliers in selections, give back the value
        cap = float(out["response_time_days"].quantile(0.99)) # get the 99th quantile, convert 99th quantile to float
        out["response_time_days"] = out["response_time_days"].clip(upper=cap) # clip off everything beyond 99th quantile


    return out.reset_index(drop=True)
