from itertools import product
import streamlit as st
import plotly.express as px
import utils

data = utils.get_data()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Oldest")
    idx = data["DOB"].idxmin()
    st.info(
        f'{data.iloc[idx]["NAME"]} - :green[{utils.calculate_age(data.iloc[idx]["DOB"])} years]')
with col2:
    st.subheader("Youngest")
    idx = data["DOB"].idxmax()
    st.info(
        f'{data.iloc[idx]["NAME"]} - :green[{utils.calculate_age(data.iloc[idx]["DOB"])} years]')

st.divider()

# --- Birthday count ---
st.subheader("Birthday count")
st.write("Check out how many birthdays fall within a time range")

dobs = data["DOB"]
date_formats = {  # keys are display options and values are strftime formats
    "Year": "%Y",
    "Month": "%b",
    "Day": "%d",
    "WeekDay": "%a",
    "Year-Month": "%Y-%b"
}
months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
years = sorted(dobs.dt.strftime("%Y").unique())
order = {
    "Year": years,
    "Month": months,
    "Day": [str(i).zfill(2) for i in range(1, 32)],
    "WeekDay": weekdays,
    "Year-Month": ["-".join(p) for p in product(years, months)]
}

how = st.selectbox("By", date_formats.keys())
# format datetimes then count
counts = dobs.dt.strftime(date_formats[how]) \
        .value_counts().rename_axis(how).reset_index()
# plotting
fig = px.bar(
    data_frame=counts,
    x=how,
    y="count",
    color=counts[how].str.slice(0, 4) if how == "Year-Month" else None,
    category_orders={how: order[how]},
    text_auto=True,
)
fig.update_traces(
    textposition="outside",
    textfont_size=14,
    hovertemplate="%{y}<extra></extra><br>%{x}"
)
fig.update_layout(
    dragmode=False,
    xaxis_tickvals=order[how],
    xaxis_ticktext=order[how],
    showlegend=how == "Year-Month",
    hovermode='closest' if how == "Year-Month" else False
)
st.plotly_chart(fig)


# --- Age Count ---
st.subheader("Age count")
st.write("This counts ages of everyone.")
ages = data['AGE'].value_counts().reset_index()
fig = px.pie(ages, values='count', names='AGE', hole=0.5)
fig.update_traces(textposition='inside', textinfo='percent+value')
st.plotly_chart(fig)