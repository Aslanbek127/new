import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from datetime import datetime

SERVER_NAME = 'DESKTOP-SGSCT58\SQLEXPRESS' 
DATABASE_NAME = 'BeautySalonDB'

class BeautySalonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Салон Красоты - Курсовая Работа")
        self.root.geometry("1100x750")
        
        # Настраиваем стили
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Цвета
        bg_color = "#f4f4f9"
        primary_color = "#34495e"
        accent_color = "#27ae60"
        
        self.root.configure(bg=bg_color)
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, font=("Arial", 11))
        self.style.configure("Header.TLabel", font=("Arial", 18, "bold"), foreground="#333")
        self.style.configure("TButton", font=("Arial", 10))
        
        # Подключение к БД
        self.conn = None
        self.connect_db()

        # Главный контейнер
        self.container = tk.Frame(root, bg=bg_color)
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def connect_db(self):
        try:
            conn_str = f'Driver={{ODBC Driver 17 for SQL Server}};Server={SERVER_NAME};Database={DATABASE_NAME};Trusted_Connection=yes;'
            self.conn = pyodbc.connect(conn_str)
        except:
            try:
                conn_str = f'Driver={{SQL Server}};Server={SERVER_NAME};Database={DATABASE_NAME};Trusted_Connection=yes;'
                self.conn = pyodbc.connect(conn_str)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Нет связи с БД: {e}")

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ==========================================
    # ЭКРАН 1: ВХОД
    # ==========================================
    def show_login_screen(self):
        self.clear_screen()
        frame = tk.Frame(self.container, bg="white", padx=50, pady=50, bd=1, relief="solid")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="ИС 'Салон Красоты'", font=("Arial", 20, "bold"), bg="white").pack(pady=20)

        tk.Button(frame, text="Я АДМИНИСТРАТОР", bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, command=self.show_admin_panel).pack(pady=10)
        
        tk.Button(frame, text="Я КЛИЕНТ", bg="#2ecc71", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, command=self.show_client_panel).pack(pady=10)

    # ==========================================
    # ЭКРАН 2: АДМИН ПАНЕЛЬ
    # ==========================================
    def show_admin_panel(self):
        self.clear_screen()
        
        # Шапка
        header = tk.Frame(self.container, bg="#2c3e50", height=60)
        header.pack(fill="x")
        tk.Button(header, text="< Выход", bg="#e74c3c", fg="white", command=self.show_login_screen).pack(side="left", padx=10, pady=10)
        tk.Label(header, text="КАБИНЕТ АДМИНИСТРАТОРА", bg="#2c3e50", fg="white", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        # Вкладки
        notebook = ttk.Notebook(self.container)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 1. Вкладка КЛИЕНТЫ (Управление)
        tab_clients = ttk.Frame(notebook)
        notebook.add(tab_clients, text=" Клиенты ")
        self.build_clients_tab(tab_clients)

        # 2. Вкладка УСЛУГИ (Управление)
        tab_services = ttk.Frame(notebook)
        notebook.add(tab_services, text=" Услуги ")
        self.build_services_tab(tab_services)

        # 3. Вкладка ЗАПИСИ (Журнал)
        tab_apps = ttk.Frame(notebook)
        notebook.add(tab_apps, text=" Журнал Записей ")
        self.build_appointments_tab(tab_apps)

        # 4. Вкладка ОТЧЕТЫ
        tab_stats = ttk.Frame(notebook)
        notebook.add(tab_stats, text=" Финансы ")
        self.build_stats_tab(tab_stats)

    # --- ЛОГИКА ВКЛАДКИ КЛИЕНТЫ ---
    def build_clients_tab(self, parent):
        # Панель инструментов
        toolbar = tk.Frame(parent, bg="#ecf0f1", pady=5)
        toolbar.pack(fill="x")
        
        tk.Button(toolbar, text="Добавить клиента", bg="#27ae60", fg="white", command=self.popup_add_client).pack(side="left", padx=5)
        tk.Button(toolbar, text="Удалить выбранного", bg="#c0392b", fg="white", command=lambda: self.delete_record("Clients", "ClientID", tree_clients)).pack(side="left", padx=5)
        tk.Button(toolbar, text="Обновить", command=lambda: self.load_clients(tree_clients)).pack(side="right", padx=5)

        # Таблица
        cols = ("ID", "Имя", "Фамилия", "Телефон", "Пол", "Дата рождения")
        tree_clients = ttk.Treeview(parent, columns=cols, show="headings")
        for col in cols: tree_clients.heading(col, text=col)
        tree_clients.pack(fill="both", expand=True)
        
        self.load_clients(tree_clients)

    def load_clients(self, tree):
        for i in tree.get_children(): tree.delete(i)
        cursor = self.conn.cursor()
        cursor.execute("SELECT ClientID, FirstName, LastName, Phone, Gender, DateOfBirth FROM Clients")
        for row in cursor.fetchall():
            tree.insert("", "end", values=list(row))

    def popup_add_client(self):
        # Всплывающее окно добавления
        top = tk.Toplevel(self.root)
        top.title("Новый клиент")
        top.geometry("300x400")
        
        tk.Label(top, text="Имя:").pack(pady=5)
        e_name = tk.Entry(top); e_name.pack()
        
        tk.Label(top, text="Фамилия:").pack(pady=5)
        e_last = tk.Entry(top); e_last.pack()
        
        tk.Label(top, text="Телефон:").pack(pady=5)
        e_phone = tk.Entry(top); e_phone.pack()
        
        tk.Label(top, text="Пол (Male/Female):").pack(pady=5)
        e_gender = ttk.Combobox(top, values=["Male", "Female"]); e_gender.pack()

        def save():
            try:
                cur = self.conn.cursor()
                cur.execute("INSERT INTO Clients (FirstName, LastName, Phone, Gender) VALUES (?, ?, ?, ?)",
                            (e_name.get(), e_last.get(), e_phone.get(), e_gender.get()))
                self.conn.commit()
                messagebox.showinfo("Ок", "Клиент добавлен!")
                top.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        tk.Button(top, text="Сохранить", bg="#27ae60", fg="white", command=save).pack(pady=20)

    # --- ЛОГИКА ВКЛАДКИ УСЛУГИ ---
    def build_services_tab(self, parent):
        toolbar = tk.Frame(parent, bg="#ecf0f1", pady=5)
        toolbar.pack(fill="x")
        tk.Button(toolbar, text="Добавить услугу", bg="#27ae60", fg="white", command=self.popup_add_service).pack(side="left", padx=5)
        tk.Button(toolbar, text="Удалить услугу", bg="#c0392b", fg="white", command=lambda: self.delete_record("Services", "ServiceID", tree_services)).pack(side="left", padx=5)
        tk.Button(toolbar, text="Обновить", command=lambda: self.load_services(tree_services)).pack(side="right", padx=5)

        cols = ("ID", "Название", "Цена", "Время (мин)")
        tree_services = ttk.Treeview(parent, columns=cols, show="headings")
        for col in cols: tree_services.heading(col, text=col)
        tree_services.pack(fill="both", expand=True)
        self.load_services(tree_services)

    def load_services(self, tree):
        for i in tree.get_children(): tree.delete(i)
        cur = self.conn.cursor()
        cur.execute("SELECT ServiceID, ServiceName, Price, DurationMinutes FROM Services")
        for row in cur.fetchall():
            price = f"{row[2]:.0f} ₸"
            tree.insert("", "end", values=(row[0], row[1], price, row[3]))

    def popup_add_service(self):
        top = tk.Toplevel(self.root)
        top.title("Новая услуга")
        top.geometry("300x300")
        
        tk.Label(top, text="Название:").pack(pady=5)
        e_name = tk.Entry(top); e_name.pack()
        tk.Label(top, text="Цена (число):").pack(pady=5)
        e_price = tk.Entry(top); e_price.pack()
        tk.Label(top, text="Длительность (мин):").pack(pady=5)
        e_dur = tk.Entry(top); e_dur.pack()

        def save():
            try:
                cur = self.conn.cursor()
                cur.execute("INSERT INTO Services (ServiceName, Price, DurationMinutes) VALUES (?, ?, ?)",
                            (e_name.get(), e_price.get(), e_dur.get()))
                self.conn.commit()
                messagebox.showinfo("Ок", "Услуга добавлена!")
                top.destroy()
            except Exception as e: messagebox.showerror("Ошибка", str(e))

        tk.Button(top, text="Сохранить", bg="#27ae60", fg="white", command=save).pack(pady=20)

    # --- УДАЛЕНИЕ ЗАПИСЕЙ ---
    def delete_record(self, table, id_col, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("!", "Выберите строку для удаления")
            return
        
        item = tree.item(selected[0])
        record_id = item['values'][0] # Берем ID из первой колонки
        
        if messagebox.askyesno("Подтверждение", f"Удалить запись ID {record_id}?"):
            try:
                cur = self.conn.cursor()
                cur.execute(f"DELETE FROM {table} WHERE {id_col} = ?", (record_id))
                self.conn.commit()
                tree.delete(selected[0])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Нельзя удалить (возможно, запись используется в другой таблице)\n{e}")

    # --- ЖУРНАЛ И СТАТИСТИКА ---
    def build_appointments_tab(self, parent):
        cols = ("ID", "Дата", "Клиент", "Услуга", "Мастер", "Статус")
        tree = ttk.Treeview(parent, columns=cols, show="headings")
        tree.column("ID", width=30)
        tree.column("Дата", width=120)
        tree.column("Клиент", width=150)
        tree.column("Услуга", width=150)
        tree.column("Мастер", width=150)
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)
        
        btn = tk.Button(parent, text="Обновить журнал", command=lambda: self.load_journal(tree))
        btn.pack(pady=5)
        self.load_journal(tree)

    def load_journal(self, tree):
        for i in tree.get_children(): tree.delete(i)
        cur = self.conn.cursor()
        query = """
            SELECT A.AppointmentID, A.AppointmentDate, 
                   C.FirstName + ' ' + C.LastName, 
                   S.ServiceName, 
                   E.FirstName + ' ' + E.LastName, 
                   A.Status
            FROM Appointments A
            JOIN Clients C ON A.ClientID = C.ClientID
            JOIN Services S ON A.ServiceID = S.ServiceID
            JOIN Employees E ON A.EmployeeID = E.EmployeeID
            ORDER BY A.AppointmentDate DESC
        """
        cur.execute(query)
        for row in cur.fetchall(): tree.insert("", "end", values=list(row))

    def build_stats_tab(self, parent):
        cols = ("Услуга", "Заказов", "Выручка")
        tree = ttk.Treeview(parent, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True)
        
        btn = tk.Button(parent, text="Пересчитать", command=lambda: self.load_stats(tree))
        btn.pack(pady=5)
        self.load_stats(tree)

    def load_stats(self, tree):
        for i in tree.get_children(): tree.delete(i)
        cur = self.conn.cursor()
        query = """
            SELECT S.ServiceName, COUNT(*), SUM(S.Price)
            FROM Appointments A
            JOIN Services S ON A.ServiceID = S.ServiceID
            WHERE A.Status = 'Completed'
            GROUP BY S.ServiceName ORDER BY SUM(S.Price) DESC
        """
        cur.execute(query)
        for row in cur.fetchall():
             rev = f"{row[2]:,.0f} ₸"
             tree.insert("", "end", values=(row[0], row[1], rev))

    # ==========================================
    # ЭКРАН 3: КЛИЕНТ
    # ==========================================
    def show_client_panel(self):
        self.clear_screen()
        
        # Шапка
        header = tk.Frame(self.container, bg="#27ae60", height=60)
        header.pack(fill="x")
        tk.Button(header, text="< Назад", bg="#2ecc71", fg="white", command=self.show_login_screen).pack(side="left", padx=10, pady=10)
        tk.Label(header, text="ОНЛАЙН ЗАПИСЬ", bg="#27ae60", fg="white", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        # Форма записи (Теперь точно появится)
        form = tk.Frame(self.container, bg="white", padx=20, pady=20)
        form.pack(pady=20, padx=20, fill="both")

        tk.Label(form, text="Выберите себя (Клиент):", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        self.cb_client = ttk.Combobox(form, width=50, state="readonly")
        self.cb_client.pack(anchor="w", pady=5)

        tk.Label(form, text="Желаемая услуга:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        self.cb_service = ttk.Combobox(form, width=50, state="readonly")
        self.cb_service.pack(anchor="w", pady=5)

        tk.Label(form, text="Мастер:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        self.cb_employee = ttk.Combobox(form, width=50, state="readonly")
        self.cb_employee.pack(anchor="w", pady=5)

        tk.Button(form, text="ЗАПИСАТЬСЯ", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), 
                  height=2, width=20, command=self.client_book).pack(pady=30)

        self.load_combos()

    def load_combos(self):
        cur = self.conn.cursor()
        
        # Клиенты
        cur.execute("SELECT ClientID, FirstName, LastName FROM Clients")
        rows = cur.fetchall()
        self.map_clients = {f"{r[1]} {r[2]}": r[0] for r in rows}
        self.cb_client['values'] = list(self.map_clients.keys())

        # Услуги
        cur.execute("SELECT ServiceID, ServiceName, Price FROM Services")
        rows = cur.fetchall()
        self.map_services = {f"{r[1]} - {r[2]:.0f} ₸": r[0] for r in rows}
        self.cb_service['values'] = list(self.map_services.keys())

        # Мастера
        cur.execute("SELECT EmployeeID, FirstName, LastName FROM Employees")
        rows = cur.fetchall()
        self.map_emps = {f"{r[1]} {r[2]}": r[0] for r in rows}
        self.cb_employee['values'] = list(self.map_emps.keys())

    def client_book(self):
        c_name = self.cb_client.get()
        s_name = self.cb_service.get()
        e_name = self.cb_employee.get()
        
        if not c_name or not s_name or not e_name:
            messagebox.showwarning("!", "Заполните все поля!")
            return

        try:
            cid = self.map_clients[c_name]
            sid = self.map_services[s_name]
            eid = self.map_emps[e_name]
            
            cur = self.conn.cursor()
            cur.execute("INSERT INTO Appointments (ClientID, EmployeeID, ServiceID, AppointmentDate, Status) VALUES (?, ?, ?, ?, 'Scheduled')",
                        (cid, eid, sid, datetime.now()))
            self.conn.commit()
            messagebox.showinfo("Успех", "Вы записаны!")
            self.show_login_screen()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BeautySalonApp(root)
    root.mainloop()