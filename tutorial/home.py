import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Data App")
# You can write anything with st.write or simply using magic.
st.write("Hello, world!")
"Hi this is magic!"

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

"Here is an interactive table:"
st.write(df)
"Here is an static table:"
st.table(df)

"You can use checkboxes to run parts of the app."
if st.checkbox("Show Pandas Dataframe"):
    "Here is display of pandas dataframe with Pandas Styler:"
    dataframe = pd.DataFrame(
        np.random.rand(10, 20), columns=("col %d" % i for i in range(20))
    )

    st.dataframe(dataframe.style.highlight_max(axis="rows"))

"Here is a line chart:"
"We can use caching to prevent regenerating data and reruning long computations."


@st.cache_data
def create_chart_data():
    return pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

chart_data = create_chart_data()
st.line_chart(chart_data)

if st.checkbox("Show map"):
    "Here is a map:"
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
    )

    st.map(map_data)

"Here is how widgets work:"
# You can assign widgets to variables.
x = st.slider("x")  # 👈 this is a widget
st.write(x, "squared is", x * x)

# Widgets can also be assessed by key.
st.text_input("Your name", key="name")
st.session_state.name, "  👈 this is a widget"

"You can use selectboxes for options: "
df = pd.DataFrame({"first_column": [1, 2, 3, 4], "second_column": [10, 20, 30, 40]})

option = st.selectbox("Which number do you like best?", df["first_column"])

"You selected: ", option

# Add a selectbox to the sidebar:
selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?", ["Email", "WhatsApp", "Phone call"]
)
st.sidebar.write("You selected: ", selectbox)

# Add a slider to the sidebar:
slider = st.sidebar.slider("Slide me", 0.0, 100.0, (25.0, 75.0))

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button("Press me!")

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        "Sorting hat", ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin")
    )
    st.write(f"You are in {chosen} house!")


"Starting a long computation..."

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f"Iteration {i+1}")
    bar.progress(i + 1)
    time.sleep(0.05)

"...and now we're done!"

"You can store values in sessions states to prevent reruning variables between different runs of the same session. See the difference between Session State and Caching."

if "scatter_df" not in st.session_state:
    st.session_state.scatter_df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("Choose a datapoint color")
color = st.color_picker("Color", "#FF0000")
st.divider()
st.scatter_chart(st.session_state.scatter_df, x="x", y="y", color=color)