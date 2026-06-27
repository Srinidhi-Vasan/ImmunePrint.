import streamlit as st

st.title("My First Streamlit App")

# Create a slider widget
number = st.slider("Select a number", 1, 10)

# Display the result
st.write(f"The square of {number} is {number ** 2}")