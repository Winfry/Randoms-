import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Load the dataset from Safricom.xlsx
df = pd.read_excel("Safaricom.xlsx")

# Clean column names
df.columns = df.columns.str.strip()

# Print the column names to verify the 'Status' column exists
print("Column names in the dataset:", df.columns)

# If the 'Status' column exists, convert it to datetime
if 'Status' in df.columns:
    # Convert the 'Status' column to datetime
    df['Status'] = pd.to_datetime(df['Status'], errors='coerce')
    print("Status column successfully parsed as datetime.")
else:
    print("Status column not found in the dataset")

# Display the dataframe to check if everything is loaded correctly
print(df.head())

# Streamlit layout
st.title("Service Pillars Progress Tracking Dashboard")

# Display the dataset in a table format
st.subheader("Dataset")
st.dataframe(df)

# Timeline visualization: Project Status over time
st.subheader("Project Status Timeline")
timeline_fig = px.timeline(df, x_start="Status", x_end="Status", y="Description",
                            color="Responsibility center", title="Project Timeline")
timeline_fig.update_yaxes(categoryorder="total ascending")  # Order by date
st.plotly_chart(timeline_fig)

# Bar chart: Projects per Responsibility Center
st.subheader("Projects by Responsibility Center")
responsibility_fig = px.bar(df, x="Responsibility center", color="Remarks", 
                            title="Projects by Responsibility Center")
st.plotly_chart(responsibility_fig)

# Pie chart: Breakdown of Project Remarks
st.subheader("Remarks Breakdown")
remarks_fig = px.pie(df, names="Remarks", title="Project Remarks Distribution")
st.plotly_chart(remarks_fig)

# Line plot: Project Status Progress over time
st.subheader("Project Status Progress over Time")
line_fig = px.line(df, x="Status", y="Description", markers=True, title="Project Status Progress")
st.plotly_chart(line_fig)

# Bar chart: Count of service pillars
st.subheader("Service Pillar Distribution")
pillar_fig = px.bar(df, x="Description", title="Distribution of Service Pillars")
st.plotly_chart(pillar_fig)

# Heatmap: Status across time (Heatmap of status dates for each project)
st.subheader("Project Status Heatmap")
# Create a pivot table for the heatmap
pivot_table = df.pivot_table(index="Description", columns="Status", values="Remarks", aggfunc="count", fill_value=0)
heatmap_fig = go.Figure(data=go.Heatmap(z=pivot_table.values, x=pivot_table.columns, y=pivot_table.index, colorscale='Viridis'))
heatmap_fig.update_layout(title="Project Status Heatmap")
st.plotly_chart(heatmap_fig)

# Scatter Plot: Status against Remarks
st.subheader("Status vs Remarks")
scatter_fig = px.scatter(df, x="Status", y="Remarks", color="Remarks", 
                         title="Scatter Plot of Status vs Remarks")
st.plotly_chart(scatter_fig)

# Add additional interactive filters (for instance, by Remark)
remark_filter = st.selectbox("Filter by Remark", df["Remarks"].unique())
filtered_df = df[df["Remarks"] == remark_filter]

st.subheader(f"Filtered Dataset (Remark: {remark_filter})")
st.dataframe(filtered_df)

# You can add more visualizations depending on the type of analysis you need
