import csv 
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

#function which saves expenses in the csv
def save_expenses(amount: str, category: str) -> bool:
    try:
        amount = float(amount)
        date = datetime.now().strftime("%Y-%m-%d")
        row = [date, amount, category]

        with open("expenses.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        return True
    
    except ValueError:
        return False
    
#after booting loads up the expenses from the csv
def load_expenses() -> list:
    expenses = []
    try:
        with open("expenses.csv", "r") as f:
            reader = csv.reader(f)
            return list(reader)
    except FileNotFoundError:
        pass

#empty the csv file for the delete function in gui
def delete_expenses():
    deletion = open("expenses.csv", "w")
    deletion.truncate()
    deletion.close()

#parse the table and return total for each category
def parse_category():
    totals = {
        "Bills" : 0.0,
        "Food" : 0.0,
        "Leisure" : 0.0,
        "Investments" : 0.0,
        "All" : 0.0
    }
    with open("expenses.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
           if len(row) != 3:
               continue
           amount = float(row[1])
           category = row[2]
           if category in totals:
                totals[category] += amount
                totals["All"] += amount
    return totals

#draw a pie chart
def pie_chart():
    pie_data = parse_category()
    pie_data.pop("All")
    keys = list(pie_data.keys())
    values = list(pie_data.values())
    fig = plt.figure(figsize=(8, 7))
    plt.pie(values, labels=keys, autopct="%1.1f%%")
    plt.show()