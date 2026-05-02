import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# --- Настройки программы ---
HISTORY_FILE = "password_history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

# --- Функции для работы с историей ---
def load_history():
    """Загружает историю паролей из файла JSON."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю паролей в файл JSON."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f)

# --- Функция генерации пароля ---
def generate_password():
    """Генерирует пароль на основе выбранных настроек."""
    length = length_var.get()
    use_digits = digits_var.get()
    use_letters = letters_var.get()
    use_special = special_var.get()

    # Проверка: выбран ли хотя бы один тип символов?
    if not (use_digits or use_letters or use_special):
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
        return

    # Формируем набор символов для генерации
    chars = ""
    if use_digits: chars += string.digits
    if use_letters: chars += string.ascii_letters
    if use_special: chars += string.punctuation

    # Генерация пароля
    password = ''.join(random.choices(chars, k=length))

    # Обновление истории и интерфейса
    history.append(password)
    save_history(history)
    update_history_table()

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# --- Функция обновления таблицы истории ---
def update_history_table():
    """Очищает и заполняет таблицу истории новыми данными."""
    for i in tree.get_children():
        tree.delete(i)
    for p in history:
        tree.insert("", "end", values=(p,))

# --- Создание главного окна ---
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("650x450")
root.resizable(False, False)

# Загрузка истории при запуске
history = load_history()

# --- Переменные Tkinter ---
length_var = tk.IntVar(value=12)
digits_var = tk.BooleanVar(value=True)
letters_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

# --- Фрейм настроек (Settings Frame) ---
settings_frame = tk.Frame(root)
settings_frame.pack(pady=10)

tk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, padx=5)
tk.Scale(settings_frame, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL,
         length=200, variable=length_var).grid(row=0, column=1, columnspan=2, padx=5)

tk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=digits_var).grid(row=1, column=0, sticky="w")
tk.Checkbutton(settings_frame, text="Буквы (a-z, A-Z)", variable=letters_var).grid(row=2, column=0, sticky="w")
tk.Checkbutton(settings_frame, text="Спецсимволы (!@#$)", variable=special_var).grid(row=3, column=0, sticky="w")

# --- Кнопка генерации ---
generate_btn = tk.Button(root, text="Сгенерировать пароль", font=("Arial", 12), command=generate_password)
generate_btn.pack(pady=15)

# --- Поле вывода пароля ---
password_entry = tk.Entry(root, font=("Consolas", 14), width=40)
password_entry.pack(pady=5)

# --- Таблица истории (Treeview) ---
tree = ttk.Treeview(root, columns=("password",), show="headings")
tree.heading("password", text="История паролей")
tree.column("password", width=600)
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Заполняем таблицу при запуске
update_history_table()

root.mainloop()
