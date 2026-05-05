import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

# Файл хранения данных
file_name = 'expenses.json'

# Главное окно и логика
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = []

        self.load()
        self.create_widgets()
        self.show_data()

    def create_widgets(self):
        # Вводные поля
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Сумма:").grid(row=0, column=0, padx=5)
        self.suma_entry = tk.Entry(frame)
        self.suma_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Категория:").grid(row=0, column=2, padx=5)
        self.cat_entry = tk.Entry(frame)
        self.cat_entry.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Дата:").grid(row=0, column=4, padx=5)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=5, padx=5)

        # Кнопка добавить
        add_btn = tk.Button(self.root, text="Добавить", command=self.add_expense)
        add_btn.pack(pady=5)

        # Таблица расходов
        self.tree = ttk.Treeview(self.root, columns=('sum', 'category', 'date'), show='headings')
        self.tree.heading('sum', text='Сумма')
        self.tree.heading('category', text='Категория')
        self.tree.heading('date', text='Дата')
        self.tree.pack(pady=10)

        # Фильтры
        frame_fil = tk.Frame(self.root)
        frame_fil.pack(pady=10)

        tk.Label(frame_fil, text="Фильтр по категории:").grid(row=0, column=0, padx=5)
        self.fil_cat = tk.Entry(frame_fil)
        self.fil_cat.grid(row=0, column=1, padx=5)

        tk.Label(frame_fil, text="Фильтр по дате:").grid(row=0, column=2, padx=5)
        self.fil_date = tk.Entry(frame_fil)
        self.fil_date.grid(row=0, column=3, padx=5)

        apply_btn = tk.Button(frame_fil, text="Показать", command=self.filter_data)
        apply_btn.grid(row=0, column=4, padx=5)

        reset_btn = tk.Button(frame_fil, text="Сброс", command=self.reset_filter)
        reset_btn.grid(row=0, column=5, padx=5)

        self.sum_label = tk.Label(self.root, text="Общая сумма: 0")
        self.sum_label.pack(pady=10)

    def add_expense(self):
        try:
            amount = float(self.suma_entry.get())
            if amount <= 0:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Положительное число для суммы.")
            return

        category = self.cat_entry.get()
        date_str = self.date_entry.get()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except:
            messagebox.showerror("Ошибка", "Формат даты ГГГГ-ММ-ДД.")
            return

        self.data.append({'sum': amount, 'category': category, 'date': date_str})
        self.save()
        self.show_data()
        self.suma_entry.delete(0, tk.END)
        self.cat_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.update_total()

    def show_data(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = data if data is not None else self.data
        for d in data:
            self.tree.insert('', tk.END, values=(d['sum'], d['category'], d['date']))

    def save(self):
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(self.data, f)

    def load(self):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except:
            self.data = []

    def filter_data(self):
        cat_filter = self.fil_cat.get().strip()
        date_filter = self.fil_date.get().strip()

        filtered = self.data
        if cat_filter:
            filtered = [d for d in filtered if d['category'] == cat_filter]
        if date_filter:
            try:
                datetime.strptime(date_filter, '%Y-%m-%d')
                filtered = [d for d in filtered if d['date'] == date_filter]
            except:
                messagebox.showerror("Ошибка", "Формат даты ГГГГ-ММ-ДД.")
                return
        self.show_data(filtered)

    def reset_filter(self):
        self.fil_cat.delete(0, tk.END)
        self.fil_date.delete(0, tk.END)
        self.show_data()

    def update_total(self):
        total = sum(d['sum'] for d in self.data)
        self.sum_label.config(text=f"Общая сумма: {total:.2f}")

# Запуск
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()