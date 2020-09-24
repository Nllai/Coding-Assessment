from flask import Flask, render_template, request, redirect
import webbrowser
import sqlite3
import pandas as pd


app = Flask(__name__)

def load_sql():
    conn = sqlite3.connect('expenses.db')
    query = 'SELECT * FROM EXPENSES'
    expenses = pd.read_sql_query(query, conn)
    expenses = expenses.to_dict(orient="index")
    conn.close()
    return expenses


def delete_sql_entry(entry):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    entry = eval(entry)
    name = entry[0]
    cost = entry[1]
    category = entry[2]
    query = f'DELETE FROM EXPENSES WHERE Name = "{name}" AND Cost = "{cost}" AND Category = "{category}"'
    c.execute(query)
    conn.commit()
    conn.close()


def add_sql_entry(name, cost, category):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    query = f'INSERT INTO EXPENSES (Name, Cost, Category) VALUES ("{name}", "{cost}", "{category}")'
    c.execute(query)
    conn.commit()
    conn.close()


@app.route('/')
def index():

    return render_template("index.html", data=load_sql())


@app.route('/delete_entry/', methods=["POST"])
def button_del():
    print(request.form['delete'])
    delete_sql_entry(request.form['delete'])
    return redirect("/")


ButtonPressed = 0
@app.route('/add_entry/', methods=["POST"])
def button_add():
    empty_check = [request.form['name'] != '', request.form['cost'] != '', request.form['category'] != '']
    if all(empty_check):
        add_sql_entry(request.form['name'], request.form['cost'], request.form['category'])
    return redirect("/")


def open_browser():
      webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == '__main__':
    open_browser()
    app.run(debug=True, port=5000)