import tkinter as tk
from tkinter import ttk
import sqlite3

# Класс главного окна.
class MainFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Хранение и инициализация объектов GUI.
    def init_main(self):
        # Создание панели инструментов(Тулбар).
        # bg - фон.
        # bd - границы.
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)

        # Упаковка.
        # Side - Закрепляет окна в вверху.
        # Fill - растягивает окно по горизонтали (X).
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Привязка изображения к кнопке Add(Добавить)
        self.add_img = tk.PhotoImage(file='./img/add.png')

        # Создание кнопки добавления.
        # bg - фон.
        # bd - границы.
        # Image - привязывание картинки к кнопке, т.е. наша иконка.
        # Command - функция по нажатию.

        btn_open_window = tk.Button(toolbar, bg='#7384F2', bd=0,
                                    image=self.add_img,
                                    command=self.open_window)
        
        # Упаковка и выравнивание по левому краю.
        btn_open_window.pack(side=tk.LEFT)

        # Добавление виджета Treeview.
        # Columns - колонки и их названия.
        # Height - высота таблицы.
        # show ='headings'- скрывает нулевую (или же пустую) колонку таблицы.
        self.tree = ttk.Treeview(self, columns=('ID', 'name',
        'tel', 'email', 'salary'), height=45, show ='headings')

        # Добавление параметров колонкам.
        # Wigth - ширина колонки.
        # Anchor - выравнивание текста, в нашем случае оно идет по центру.
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # Подписи колонок.
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Full name')
        self.tree.heading('tel', text='Phone number')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Salary')

        # Упаковка и выравнивание по левому краю.
        self.tree.pack(side=tk.LEFT)

        # Добавление возможности двигать содержимое вверх или вниз.
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        
        #Создание кнопки редактирования.
        self.update_image = tk.PhotoImage(file='./img/update.png')
        btn_edit_window = tk.Button(toolbar, bg='#F2DE73',
                                    bd=0, image=self.update_image,
                                    command=self.open_update_window)
        
        # Упаковка и выравнивание по левому краю.
        btn_edit_window.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#F2737C', bd=0,
                               image=self.delete_img, 
                               command=self.delete_records)
        
        # Упаковка и выравнивание по левому краю.
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#F2C673', bd=0,
                              image=self.search_img,
                              command=self.open_search_window)
        
        # Упаковка и выравнивание по левому краю.
        btn_search.pack(side=tk.LEFT)

        # Создание кнопки обновления.
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#BE73F2', bd=0,
                                image=self.refresh_img,
                                command=self.view_records)
        
        # Упаковка и выравнивание по левому краю.
        btn_refresh.pack(side=tk.LEFT)

    # Метод, отвечающий за поиск записей в таблице.
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
        for row in self.db.c.fetchall()]

    # Метод, отвечающий за вызов дочернего окна
    def open_window(self):
        EmployeeFrame()

    # Добавление данных.
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Вывод данных в виджет таблицы.
    def view_records(self):
        # Выбор информации из базы данных.
        self.db.c.execute('''SELECT * FROM db''')
        # Удаление всего из виджета таблицы.
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Добавление в виджет таблицы информации из базы данных.
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    # Метод, отвечающий за вызов дочернего окна
    def open_update_window(self):
        UpdateEmployeeDataFrame ()

    # Метод, отвечающий за обновление записей из таблицы.
    def update_records(self, name, tel, email, salary):
        self.db.c.execute('''UPDATE db SET name = ?, tel = ?, email = ?, salary = ?
        WHERE ID = ?''', (name, tel, email, salary,
        self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Метод, отвечающий за удаление записей из таблицы.
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM db WHERE id = ?''',
            (self.tree.set(selection_item, '#1'),))
        
        self.db.conn.commit()
        self.view_records()

    # Метод, отвечающий за вызов дочернего окна.
    def open_search_window(self):
        SearchEmployeeFrame()

# Класс дочерних окон.
# Toplevel - окно верхневого уровня.
class EmployeeFrame(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app

        self.title('Add')
        self.geometry('400x220')
        # Ограничение изменения размеров окна.
        self.resizable(False, False)
        # Перехват всех событий, происходящих в приложении.
        self.grab_set()
        # Захватывание фокуса.
        self.focus_set()

        # Подписи.
        label_name = tk.Label(self, text='Full Name:')
        label_name.place(x=50, y= 30)

        label_select = tk.Label(self, text='Phone number:')
        label_select.place(x=50, y=60)

        label_sum = tk.Label(self, text='E-mail:')
        label_sum.place(x=50, y=90)

        label_sal = tk.Label(self, text='Salary:')
        label_sal.place(x=50, y=120)

        # Добавление строки ввода для наименования.
        self.entry_name = ttk.Entry(self)
        # Изменение координатов объекта.
        self.entry_name.place(x=200, y=30)

        # Добавление строки ввода для почты.
        self.entry_email = ttk.Entry(self)
        # Изменение координатов объекта.
        self.entry_email.place(x=200, y=60)

        # Добавление строки ввода для номера телефона.
        self.entry_tel = ttk.Entry(self)
        # Изменение координатов объекта.
        self.entry_tel.place(x=200, y=90)


        # Добавление строки ввода для зарплаты.
        self.entry_salary= ttk.Entry(self)
        # Изменение координатов объекта.
        self.entry_salary.place(x=200, y=120)


        # Кнопка закрытия дочернего окна.
        self.btn_cancel = ttk.Button(self, text='Close',
                                      command=self.destroy)
        self.btn_cancel.place(x=270, y=170)
        
        # Кнопка добавления.
        self.btn_Add = ttk.Button(self, text='Add')
        self.btn_Add.place(x=190, y=170)
        # Срабатывание по ЛКМ.
        # При нажатии кнопки вызывается метод records, которому передаются все значения.
        self.btn_Add.bind('<Button-1>', lambda event:
                        self.view.records(self.entry_name.get(),
                                          self.entry_email.get(),
                                          self.entry_tel.get(),
                                          self.entry_salary.get()))


class UpdateEmployeeDataFrame(EmployeeFrame):
    def __init__(self):
        super().__init__()
        self.view = app
        self.db = db
        self.default_data()

        # Создание кнопки обновления таблицы.
        self.title('Edit Position')
        btn_edit = ttk.Button(self, text='Edit')
        btn_edit.place(x=300, y=170)
        btn_edit.bind("<Button-1>", lambda event:
                      self.view.update_records(self.entry_name.get(),
                                               self.entry_email.get(),
                                               self.entry_tel.get(),
                                               self.entry_salary.get()))
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add='+')
        self.btn_Add.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE
        id = ?''',
        (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# Создание кнопки поиска записей.
class SearchEmployeeFrame(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app

        self.title('Search')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Search')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Search')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        # Создаем соединение с базой данных.
        self.conn = sqlite3.connect('db.db')
        # Создание объекта класса cursor, используемые для взаимодействия с БД.
        self.c = self.conn.cursor()
        # Выполнение запроса к БД.
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS db (id INTEGER PRIMARY KEY,
            name TEXT, tel TEXT, email TEXT, salary TEXT)''')
        # Сохранение изменения БД.
        self.conn.commit()

    # Метод добавления в БД.
    def insert_data(self, name, tel, email, salary):
        self.c.execute('''INSERT INTO db (name, tel, email, salary) VALUES(?, ?, ?, ?)''', 
                       (name, tel, email, salary))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    # Экземпляр класса DB.
    db = DB()
    app = MainFrame(root)
    # Упаковка.
    app.pack() 
    # Заголовок окна.
    root.title('Phone Book')
    # Размер окна.
    root.geometry('900x400')
    # Ограничение изменения размеров окна.
    root.resizable(False, False)
    root.mainloop()




      