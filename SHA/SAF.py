import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load the dataset
df = pd.read_excel("Safaricom.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Ensure date parsing
df['Status'] = pd.to_datetime(df['Status'], errors='coerce')

# Add default End Date if missing
if "End Date" not in df.columns:
    df["End Date"] = df["Status"] + pd.Timedelta(days=1)

# Streamlit App Layout
st.title("Investor Dashboard: Service Pillars Progress Tracker")

# KPI Section
st.subheader("Key Metrics")
total_projects = df["Description"].nunique()
completed_projects = df[df["Remarks"] == "Completed"].shape[0]
pending_projects = df[df["Remarks"] == "Pending"].shape[0]
upcoming_deadlines = df[df["Status"] > datetime.now()].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Projects", total_projects)
col2.metric("Completed", completed_projects)
col3.metric("Pending", pending_projects)
col4.metric("Upcoming Deadlines", upcoming_deadlines)

# Filters
st.sidebar.header("Filters")
responsibility_filter = st.sidebar.multiselect(
    "Responsibility Center", 
    df["Responsibility center"].unique(), 
    default=df["Responsibility center"].unique()
)
remarks_filter = st.sidebar.multiselect(
    "Remarks", 
    df["Remarks"].unique(), 
    default=df["Remarks"].unique()
)
date_filter = st.sidebar.date_input(
    "Select Date Range", 
    [df["Status"].min(), df["Status"].max()]
)

# Apply Filters
filtered_df = df[
    (df["Responsibility center"].isin(responsibility_filter)) &
    (df["Remarks"].isin(remarks_filter)) &
    (df["Status"].between(date_filter[0], date_filter[1]))
]

# Dataset Preview
st.subheader("Filtered Dataset")
st.dataframe(filtered_df)

# Visualizations
st.subheader("Visualizations")

# Gantt Chart
st.markdown("### Gantt Chart")
if not filtered_df.empty:
    gantt_chart = px.timeline(
        filtered_df,
        x_start="Status",
        x_end="End Date",
        y="Description",
        color="Remarks",
        title="Project Timeline"
    )
    gantt_chart.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(gantt_chart)
else:
    st.warning("No data available for the selected filters.")

# Remarks Breakdown
st.markdown("### Remarks Breakdown")
if not filtered_df.empty:
    remarks_fig = px.pie(filtered_df, names="Remarks", title="Remarks Distribution")
    st.plotly_chart(remarks_fig)

# Responsibility Center Breakdown
st.markdown("### Responsibility Center Breakdown")
if not filtered_df.empty:
    responsibility_fig = px.bar(
        filtered_df, 
        x="Responsibility center", 
        color="Remarks", 
        title="Projects by Responsibility Center"
    )
    st.plotly_chart(responsibility_fig)

# Detailed Breakdown
st.markdown("### Project Details")
for idx, row in filtered_df.iterrows():
    st.write(f"**Project:** {row['Description']}")
    st.write(f"- Responsibility Center: {row['Responsibility center']}")
    st.write(f"- Status: {row['Status']}")
    st.write(f"- End Date: {row['End Date']}")
    st.write(f"- Remarks: {row['Remarks']}")
    st.markdown("---")

# Heatmap (Optional for Investors)
st.markdown("### Heatmap: Status Across Time")
pivot_table = filtered_df.pivot_table(
    index="Description", 
    columns="Status", 
    values="Remarks", 
    aggfunc="count", 
    fill_value=0
)
heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=pivot_table.values, 
        x=pivot_table.columns, 
        y=pivot_table.index, 
        colorscale="Viridis"
    )
)
heatmap_fig.update_layout(title="Status Heatmap")
st.plotly_chart(heatmap_fig)
