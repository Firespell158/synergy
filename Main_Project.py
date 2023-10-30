import tkinter as tk 
from tkinter import ttk
import sqlite3


# Класс нового окна


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()


    # Инициализируем виджеты для главного окна

    def init_main(self):
        toolbar = tk.Frame(bg="#d7d7d7", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Кнопка добавления

        self.img_add = tk.PhotoImage(file="add.png")
        btn_add = tk.Button(toolbar, text="Добавить", bg="#d7d7d7",
                            bd = 0, image=self.img_add,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Кнопка изменения

        self.img_upd = tk.PhotoImage(file="change.png")
        btn_upd = tk.Button(toolbar, bg="#d7d7d7",
                            bd = 0, image=self.img_upd,
                            command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)

        # Кнопка поиска
        self.img_search = tk.PhotoImage(file="search.png")
        btn_search = tk.Button(toolbar, bg="#d7d7d7", 
                               bd = 0, image=self.img_search,
                               command=self.open_searc)
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления
        self.img_refresh = tk.PhotoImage(file="refresh.png")
        btn_refresh = tk.Button(toolbar, bg="#d7d7d7",
                                bd = 0, image=self.img_refresh,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        #Кнопка удаления
        btn_del = tk.Button(toolbar, text="Удалить",
                            bg="#d7d7d7", bd=0,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # Таблица

        self.tree = ttk.Treeview(root,
                                 columns=("id","name","phone","email", "salary"),
                                 height=45,
                                 show="headings")
        
        self.tree.column("id", width=45, anchor=tk.CENTER)
        self.tree.column("name", width=150, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        self.tree.heading("id", text="id")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Электронная-Почта")
        self.tree.heading("salary", text="зарплата")

        self.tree.pack(side=tk.LEFT)

        # добавление скроллбара
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления данных

    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # Отображение данных в treeview

    def view_records(self):
        self.db.cur.execute("SELECT * FROM users")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    # Метод поиска данных

    def search_records(self, name):
        self.db.cur.execute("SELECT * FROM users WHERE name LIKE ?",
                            ("%" + name + "%", ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    # Метод изменения данных
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], "#1")
        self.db.cur.execute("""
            UPDATE users
            SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        """, (name, phone, email, salary, id))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления строк
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute("DELETE FROM users WHERE id = ?",
                                (self.tree.set(row, "#1"), ))
            
            self.db.conn.commit()
            self.view_records()

    # Метод вызывающий дочернее окно

    def open_child(self):
        Child()

    # Метод вызывающий дочернее окно для редактирования

    def open_update_child(self):
        Update()

    # Метод вызывающий дочернее окно для поиска данных

    def open_searc(self):
        Search()


# Класс дочернего окна

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализируем виджеты для дочернего окна
    def init_child(self):
        self.title("Добавление сотрудника")
        self.geometry("400x200")
        self.resizable(False, False)

        # Перехватываем все события

        self.grab_set()

        # Перехватываем фокус

        self.focus_set()

        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=50, y=50)
        label_name = tk.Label(self, text="Телефон")
        label_name.place(x=50, y=80)
        label_name = tk.Label(self, text="E-mail")
        label_name.place(x=50, y=110)
        label_name = tk.Label(self, text="зарплата")
        label_name.place(x=50, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=200, y=170)

        self.btn_add = tk.Button(self, text="Добавить")
        self.btn_add.bind("<Button-1>", lambda ev: self.view.records(self.entry_name.get(),
                                                                self.entry_phone.get(),
                                                                self.entry_email.get(),
                                                                self.entry_salary.get()))
        self.btn_add.place(x=265, y=170)

        # класс дочернего окна для изменения данных

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title("Изменение контакта")
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text="Изменить")
        self.btn_upd.bind("<Button-1>",
                     lambda ev: self.view.update_record(self.entry_name.get(),
                                                        self.entry_phone.get(),
                                                        self.entry_email.get(),
                                                        self.entry_salary.get()))
        self.btn_upd.bind("<Button-1>", lambda ev: self.destroy(), add="+")
        self.btn_upd.place(x=265, y=170)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], "#1")
        self.db.cur.execute("SELECT * from users WHERE id = ?", (id, ))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # инициализация виджетов дочернего окна

    def init_child(self):
        self.title("Поиск сотрудника")
        self.geometry("300x100")
        self.resizable(False, False)

        self.grab_set()

        self.focus_set()

        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=30, y=30)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=130, y=30)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=150, y=70)

        self.btn_add = tk.Button(self, text="Найти")
        self.btn_add.bind("<Button-1>",
                          lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_add.bind("<Button-1>", lambda ev: self.destroy(), add = "+")
        self.btn_add.place(x=225, y=70)
            

# Класс БД
class Db:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("contacts.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT,
                         salary INTEGER
        )""")
        self.conn.commit()

    def insert_data(self, name, phone, email, salary):
        self.cur.execute("""
                         INSERT INTO users (name, phone, email, salary)
                         Values (?, ?, ?, ?)""", (name, phone, email, salary))
        self.conn.commit()

# При запуске программы
if __name__ == "__main__":
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title("список сотрудников")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()
