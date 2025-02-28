import streamlit as st
import sqlite3
from streamlit_option_menu import option_menu

def connectdb():
    conn=sqlite3.connect("mydb.db")
    return conn

def createTable():
    with connectdb() as conn:
        cur=conn.cursor()
        cur.execute("Create table if not exists student(name text,passord text,roll int primary key,branch text)")
        conn.commit()

def add_record(data):
    with connectdb() as conn:
        cur=conn.cursor()
        try:
            cur.execute("Insert into student(name,passord,roll,branch) values(?,?,?,?)",data)
            conn.commit()
        except sqlite3.IntegrityError:
            st.error("Student already registered")

def display():
    with connectdb() as conn:
        cur=conn.cursor()
        cur.execute("Select * from student")
        result=cur.fetchall()
        return result
    

def signup():
    st.title("Registration Form")
    name=st.text_input("Enter your Name:")
    password=st.text_input("Enter your password:",type="password")
    repassword=st.text_input("Enter your password again:",type="password")
    roll=st.number_input("Enter your Roll no:",format='%0.0f')
    branch=st.selectbox("Select Branch:",options=["CSE","AIML"])
    if st.button("Signin"):
        if password!=repassword:
            st.warning("Password Mismatched")
        else:
            add_record((name,password,roll,branch))
            st.success("Student Registered Successfully!!")

createTable()
with st.sidebar:
    selected=option_menu("My App",['Signup','Display all record'],icons=['box-arrow-in-left','table'],menu_icon="./images/user.png")

if selected=='Signup':
    signup()
else:
    data=display()
    st.table(data)