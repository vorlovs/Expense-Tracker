import tkinter as tk
import csv
from tkinter import ttk
from logic import save_expenses, load_expenses, delete_expenses, parse_category, pie_chart 

def run_app():
    #center the window
    root = tk.Tk()
    root.title("Expenses Tracker 1.0")
    window_width = 650
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    #basic stuff for looks
    tk.Label(root, text="Amount spent:").grid(row=0, column=0, padx=5, pady=5)
    entry_amount = tk.Entry(root)
    entry_amount.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Category:").grid(row=0, column=2, padx=5, pady=5)
    combo_category = ttk.Combobox(root, state='readonly', values=["Food", "Bills", "Leisure", "Investments"])
    combo_category.set("Select a category")
    combo_category.grid(row=0, column=3, padx=5, pady=5)

    #function for button to save whats written, the button is below too
    def on_save():
        amount = entry_amount.get()
        category = combo_category.get()
        if combo_category.get() == "Select a category":
            print("Invalid category!")
        else:
            if save_expenses(amount, category):
                update_table()
                entry_amount.delete(0, tk.END)
                combo_category.set("Select a category")
            else:
                print("Invalid input!")

    save_btn = tk.Button(root, text="Add", command=on_save)
    save_btn.grid(row=1, column=0, columnspan=4, pady=15)

    #ttk table creation and filling it up
    columns = ("date", "amount", "category")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("date", text="Date")
    tree.heading("amount", text="Amount")
    tree.heading("category", text="Category")
    tree.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

    #category filter
    tk.Label(root, text="Filter by category:").grid(row=3, column=0, padx=5, pady=10, sticky="w")
    filter_combo = ttk.Combobox(root, state='readonly', values=["All", "Food", "Bills", "Leisure", "Investments"])
    filter_combo.set("All")
    filter_combo.grid(row=3, column=1, padx=5, pady=10, sticky="w")
    
    #result label
    result_label = tk.Label(root, text="")
    result_label.grid(row=3, column=4, columnspan=5, pady=10)
    
    #clear table button and function for it
    def on_click_delete(event):
        tree.delete(*tree.get_children())
        delete_expenses()

    
    clear_btn = ttk.Button(root, text="Clear table")
    clear_btn.bind("<Button-1>", on_click_delete)
    clear_btn.grid(row=3, column=3, padx=5, pady=5)
   
    #function for total button for various categories
    def show_category_total(event):
        parsing = parse_category()
        show_total_category = str(filter_combo.get())    
        category_get = parsing.get(f"{show_total_category}")
        result_label.grid(row=4, column=1, padx=5, pady=5)
        result_label.config(text=f"Total spent on {show_total_category} {category_get} EUR")
       

    #total button with 2 modes of working
    btn_total = tk.Button(root, text="Show Total")
    btn_total.bind("<Button-1>", show_category_total)
    btn_total.grid(row=3, column=2, padx=5, pady=5)

    #update table
    def update_table():
        for row in tree.get_children():
            tree.delete(row)
        for row in load_expenses():
            if len(row) == 3:
                tree.insert("", tk.END, values=row)
                
    #button for pie chart
    btn_chart = tk.Button(root, text="Show pie chart", command=pie_chart)
    btn_chart.grid(row=5, column=0, padx=5, pady=5)


    update_table()
    root.mainloop()

