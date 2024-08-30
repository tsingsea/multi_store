import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


# 读取Excel数据
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Excel file: {str(e)}")
        return None


# 计算价格
def calculate_price(sales_amount, sales_quantity, input_quantity):
    price = (sales_amount / (sales_quantity * 1000)) * input_quantity
    return price


# 更新显示的记录列表
def update_display():
    for widget in display_frame.winfo_children():
        widget.destroy()

    total_price = 0
    for index, record in enumerate(records):
        total_price += record['price']
        label = tk.Label(display_frame, text=f"{record['name']} {record['quantity']}g: ¥{record['price']:.2f}")
        label.grid(row=index, column=0, sticky="w")

        delete_button = tk.Button(display_frame, text="Delete", command=lambda i=index: delete_record(i))
        delete_button.grid(row=index, column=1, padx=5)

    total_label = tk.Label(display_frame, text=f"\nTotal: ¥{total_price:.2f}")
    total_label.grid(row=len(records), column=0, sticky="w")


# 搜索功能
def search():
    name = search_var.get()
    quantity = quantity_var.get()
    if not name or not quantity:
        messagebox.showwarning("Input Error", "Please enter both name and quantity")
        return

    try:
        quantity = float(quantity)
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number for quantity")
        return

    row = data[data['通用名'] == name]
    if row.empty:
        messagebox.showwarning("Not Found", "Name not found in data")
        return

    sales_amount = row['销售金额'].values[0]
    sales_quantity = row['销售数量'].values[0]
    price = calculate_price(sales_amount, sales_quantity, quantity)

    records.append({'name': name, 'quantity': quantity, 'price': price})
    update_display()


# 更新下拉列表选项
def update_options(event):
    input_text = search_var.get()
    if input_text:  # 只有在有输入时才更新选项
        matching_options = data[data['通用名'].str.contains(input_text, case=False, na=False)]['通用名'].tolist()
        search_combobox['values'] = matching_options
        search_combobox.event_generate('<Down>')  # 自动显示下拉列表
    else:
        search_combobox['values'] = []  # 如果没有输入，清空选项


# 删除记录
def delete_record(index):
    records.pop(index)
    update_display()


# GUI部分
app = tk.Tk()
app.title("Price Calculator")

# 搜索框和数量输入
search_var = tk.StringVar()
quantity_var = tk.StringVar()

tk.Label(app, text="Search Name:").grid(row=0, column=0, padx=5, pady=5)

# 使用Combobox替代Entry
search_combobox = ttk.Combobox(app, textvariable=search_var)
search_combobox.grid(row=0, column=1, padx=5, pady=5)
search_combobox.bind('<KeyRelease>', update_options)  # 绑定键盘事件，用于实时更新选项

tk.Label(app, text="Quantity (g):").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(app, textvariable=quantity_var).grid(row=1, column=1, padx=5, pady=5)

tk.Button(app, text="Calculate", command=search).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# 显示结果的Frame
display_frame = tk.Frame(app)
display_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# 初始化
file_path = 'data.xlsx'  # 替换为你的Excel文件路径
data = load_data(file_path)
records = []

app.mainloop()