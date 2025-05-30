import sqlite3
import string
import tkinter as tk
from tkinter import messagebox
import random

#Banco de dados
def init_db():
    conn = sqlite3.connect("senhas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS senhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_password_to_db(website, username, password):
    conn = sqlite3.connect("senhas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO senhas (website, username, password) VALUES (?, ?, ?)", (website, username, password))
    conn.commit()
    conn.close()

def search_password_from_db(website):
    conn = sqlite3.connect("senhas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM senhas WHERE website = ?", (website,))
    result = cursor.fetchone()
    conn.close()
    return result

def add_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not username or not password:
        messagebox.showwarning("Aviso", "Todos os campos são obrigatórios!")
        return

    add_password_to_db(website, username, password)
    messagebox.showinfo("Sucesso", "Senha salva com sucesso!")
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def search_password():
    website = website_entry.get().strip()
    if not website:
        messagebox.showwarning("Aviso", "Informe o site para buscar.")
        return

    result = search_password_from_db(website)
    if result:
        username, password = result
        messagebox.showinfo("Senha encontrada", f"Website: {website}\nUsuário: {username}\nSenha: {password}")
    else:
        messagebox.showerror("Erro", f"Nenhum dado encontrado para: {website}")

def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    random_password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, random_password)

#Interface
root = tk.Tk()
root.title("Gerenciador de Senhas")
root.geometry("500x420")
root.configure(bg="#3c3f41")
root.resizable(False, False)

FONT_LABEL = ("Segoe UI", 10)
FONT_ENTRY = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_BTN = ("Segoe UI", 10, "bold")

def create_entry(parent):
    return tk.Entry(parent, font=FONT_ENTRY, bg="white", fg="black", insertbackground="black", relief="flat", highlightthickness=1)

def create_button(parent, text, command):
    return tk.Button(parent, text=text, command=command, font=FONT_BTN, bg="white", fg="black", activebackground="#e0e0e0", relief="flat", width=20)

frame = tk.Frame(root, bg="#3c3f41", padx=20, pady=20)
frame.pack(expand=True)

tk.Label(frame, text="Gerenciador de Senhas", bg="#3c3f41", fg="white", font=FONT_TITLE).pack(pady=(0, 20))

tk.Label(frame, text="Website:", bg="#3c3f41", fg="white", font=FONT_LABEL).pack(anchor="w", pady=(5, 0))
website_entry = create_entry(frame)
website_entry.pack(fill="x", pady=(0, 10))

tk.Label(frame, text="Usuário:", bg="#3c3f41", fg="white", font=FONT_LABEL).pack(anchor="w", pady=(5, 0))
username_entry = create_entry(frame)
username_entry.pack(fill="x", pady=(0, 10))

tk.Label(frame, text="Senha:", bg="#3c3f41", fg="white", font=FONT_LABEL).pack(anchor="w", pady=(5, 0))
password_entry = create_entry(frame)
password_entry.pack(fill="x", pady=(0, 10))

btn_frame = tk.Frame(frame, bg="#3c3f41")
btn_frame.pack(pady=15)

create_button(btn_frame, "Gerar Senha", generate_password).pack(pady=5)
create_button(btn_frame, "Salvar Senha", add_password).pack(pady=5)
create_button(btn_frame, "Buscar Senha", search_password).pack(pady=5)

init_db()
root.mainloop()
