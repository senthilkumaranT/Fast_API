import streamlit as st
import json 
import requests
from main import calculator_api

st.title("Calculator")


option = st.selectbox("Select the operation", ("Addition", "Subtraction", "Multiplication", "Division"))

st.write("select the number in the below slider")

x = st.slider("Number 1", 0, 100, 1)
y = st.slider("Number 2", 0, 100, 1)


input = {"x" :x, "y" :y  , "operation" : option}


if st.button("calculate"):
    headers = {"Content-Type": "application/json"}
    res = requests.post(
        url="http://localhost:8000/calculator", 
        json=input,
        headers=headers
    )
    
    st.subheader(f"The result of the operation is:  = {res.text} ")

