from tkinter import ttk, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label, Frame
from tkinter import font as tkfont
import tkinter as tk
from kegiatan import Kegiatan
from kategori import Kategori
from tkinter import messagebox
from datetime import datetime
from model_app import Model
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        ## CONNECT DATABASE
        Model.create_table(self)   ## udah dibikin

        ## VARIABEL
        #### Variabel Tambah Kegiatan
        self.INPUT_NAMA_KEGIATAN = tk.StringVar()
        self.INPUT_BATAS_WAKTU = tk.StringVar()
        self.INPUT_KATEGORI = tk.StringVar()
        #### Variabel Tambah Kategori
        self.INPUT_NAMA_KATEGORI = tk.StringVar()
        #### Variabel Filter Kegiatan
        self.INPUT_FILTER_STATUS = tk.StringVar()
        self.INPUT_FILTER_WAKTU = tk.StringVar()
        self.INPUT_FILTER_KATEGORI = tk.StringVar()

        ## SETUP GUI
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = int(width / 2 - 960 / 2)
        y = int(height / 2 - 600 / 2 - 40)
        geometry = '960x600+' + str(x) + '+' + str(y)
        self.geometry(geometry)
        self.resizable(False, False)

        ## BACKGROUND
        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 600,
            width = 960,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            100.0,
            299.0,
            860.0,
            522.0,
            fill="#D9D9D9",
            outline="")

        ## TABLE / TREE VIEW
        ##### Define Table Frame
        self.table_frame = Frame(self, bg='red')
        self.table_frame.place(x=78, y=300)
        #### Define Columns
        columns = ('id_kegiatan', 'nama_kegiatan', 'batas_waktu', 'kategori', 'status')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        #### Define Headings
        self.tree.heading('id_kegiatan', text='ID')
        self.tree.column('id_kegiatan', minwidth=0, width=0)
        self.tree.heading('nama_kegiatan', text='Kegiatan')
        self.tree.column('nama_kegiatan', minwidth=0, width=340)
        self.tree.heading('batas_waktu', text='Batas Waktu')
        self.tree.column('batas_waktu', minwidth=0, width=150)
        self.tree.heading('kategori', text='Kategori')
        self.tree.column('kategori', minwidth=0, width=150)
        self.tree.heading('status', text='Status')
        self.tree.column('status', minwidth=0, width=150)
        #### Define Place
        self.tree.grid(row=0, column=0, sticky='nsew')
        #### Add Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        #### Rendering Data
        self.render_data_kegiatan_all()
        
        ## BUTTON DELETE
        self.button_image_del = ImageTk.PhotoImage(Image.open("./assets/button_del.png"))
        self.button_del = Button(
            image=self.button_image_del,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_kegiatan,
            relief="flat"
        )
        self.button_del.place(
            x=730.0,
            y=247.0,
            width=130.0,
            height=36.0
        )

        ## BUTTON MARK AS DONE
        self.button_image_done = ImageTk.PhotoImage(Image.open("./assets/button_done.png"))
        #  self.button_image_done = PhotoImage(
        #     file="./assets/button_done.png")
        self.button_done = Button(
            image=self.button_image_done,
            borderwidth=0,
            highlightthickness=0,
            command=self.tandai_selesai_kegiatan,
            relief="flat"
        )
        self.button_done.place(
            x=592.0,
            y=247.0,
            width=130.0,
            height=36.0
        )

        ## BUTTON FILTER
        self.button_image_filter = ImageTk.PhotoImage(Image.open("./assets/button_filter.png"))
        # self.button_image_filter = PhotoImage(
        #     file="./assets/button_filter.png")
        self.button_filter = Button(
            image=self.button_image_filter,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_pop_up_filter,
            relief="flat"
        )
        self.button_filter.place(
            x=100.0,
            y=247.0,
            width=76.0,
            height=36.0
        )

        ## LINE DIVIDER
        canvas.create_rectangle(
            99.0,
            230.0,
            860.0,
            231.0,
            fill="#263238",
            outline="")

        ## BUTTON TAMBAH KATEGORI
        self.button_image_kategori = ImageTk.PhotoImage(Image.open("./assets/button_kategori.png"))
        # self.button_image_kategori = PhotoImage(
        #     file="./assets/button_kategori.png")
        self.button_kategori = Button(
            image=self.button_image_kategori,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_pop_up_kategori,
            relief="flat"
        )
        self.button_kategori.place(
            x=484.0,
            y=179.0,
            width=156.0,
            height=36.0
        )

        ## BUTTON TAMBAH KEGIATAN
        self.button_image_kegiatan = ImageTk.PhotoImage(Image.open("./assets/button_kegiatan.png"))
        # self.button_image_kegiatan = PhotoImage(
        #     file="./assets/button_kegiatan.png")
        self.button_kegiatan = Button(
            image=self.button_image_kegiatan,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_pop_up_kegiatan,
            relief="flat"
        )
        self.button_kegiatan.place(
            x=320.0,
            y=179.0,
            width=156.0,
            height=36.0
        )

        ## HEADER
        canvas.create_rectangle(
            0.0,
            0.0,
            960.0,
            138.0,
            fill="#FFC107",
            outline="")
        canvas.create_text(
            338.0,
            105.0,
            anchor="nw",
            text="Aplikasi To Do List Asisten Harianmu",
            fill="#263238",
            font=("Lexend Regular", 16 * -1)
        )
        self.logo = ImageTk.PhotoImage(Image.open("./assets/logo.png"))
        # self.logo = PhotoImage(
        #     file="./assets/logo.png")
        self.image_logo = canvas.create_image(
            480.0,
            65.0,
            image=self.logo
        )
    
    def show_pop_up_kegiatan(self):
        self.pop_up = Toplevel(self)
        list_kategori = self.get_list_kategori()
        print(list_kategori)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = int(width / 2 - 300 / 2)
        y = int(height / 2 - 442 / 2 - 40)
        geometry = '300x442+' + str(x) + '+' + str(y)
        self.pop_up.geometry(geometry)
        self.pop_up.title("Tambah Kegiatan")

        self.pop_up_frame = Frame(self.pop_up)
        self.pop_up_frame.pack(fill=tk.BOTH)

        self.label_title = Label(self.pop_up_frame, text = "Tambah Kegiatan", font=("Segoe UI Semibold", 16), bg='#FFA000', fg='#263238')
        self.label_title.pack(ipady=10, fill=tk.X)
        
        self.pop_up_frame_content = Frame(self.pop_up)
        self.pop_up_frame_content.pack(padx=40, pady=8, fill=tk.BOTH)

        fields = {}
        fields['label_kegiatan'] = Label(self.pop_up_frame_content, text='Nama Kegiatan:', font=("Segoe UI Semibold", 12))
        fields['entry_kegiatan'] = Entry(self.pop_up_frame_content, textvariable=self.INPUT_NAMA_KEGIATAN, width= 40, bg='#CFD8DC', fg='#455A64', font=("Segoe UI", 12))
        fields['label_batas_waktu'] = Label(self.pop_up_frame_content, text='Batas Waktu YYYY-MM-DD:', font=("Segoe UI Semibold", 12))
        fields['entry_batas_waktu'] = Entry(self.pop_up_frame_content, textvariable=self.INPUT_BATAS_WAKTU, width= 40, bg='#CFD8DC', fg='#455A64', font=("Segoe UI", 12))
        fields['label_kategori'] = Label(self.pop_up_frame_content, text='Kategori:', font=("Segoe UI Semibold", 12))
        fields['entry_kategori'] = ttk.Combobox(self.pop_up_frame_content, values=list_kategori, state='readonly', textvariable=self.INPUT_KATEGORI, width= 40, font=("Segoe UI", 12))

        for field in fields.values():
            field.pack(anchor=tk.W, padx=12, pady=4, ipady=4)
        
        self.button_kirim = Button(self.pop_up_frame_content, text="Kirim", bg='#FFCC80', font=("Segoe UI Semibold", 10), command=self.submit_kegiatan)
        self.button_kirim.pack(ipadx=78, ipady=2, pady=32)

    def show_pop_up_kategori(self):
        self.pop_up = Toplevel(self)
        # self.controller = controller
        # self.id = controller.id
        self.pop_up_font = tkfont.Font(family="Lexend SemiBold", size = 16, weight = "bold")
        
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = int(width / 2 - 300 / 2)
        y = int(height / 2 - 202 / 2 - 40)
        geometry = '300x222+' + str(x) + '+' + str(y)
        self.pop_up.geometry(geometry)
        self.pop_up.resizable(False, False)
        self.pop_up.title("Tambah Kategori")
        
        self.pop_up_frame = Frame(self.pop_up)
        self.pop_up_frame.pack(fill=tk.BOTH)

        self.label_title = Label(self.pop_up_frame, text = "Tambah Kategori", font=("Segoe UI Semibold", 16), bg='#FFA000', fg='#263238')
        self.label_title.pack(ipady=10, fill=tk.X)
        
        self.pop_up_frame_content = Frame(self.pop_up)
        self.pop_up_frame_content.pack(padx=40, pady=8, fill=tk.BOTH)

        fields = {}
        fields['label_kategori'] = Label(self.pop_up_frame_content, text='Nama Kategori :', font=("Segoe UI Semibold", 12))
        fields['entry_kategori'] = Entry(self.pop_up_frame_content, textvariable=self.INPUT_NAMA_KATEGORI, width= 40, bg='#CFD8DC', fg='#455A64', font=("Segoe UI", 12))

        for field in fields.values():
            field.pack(anchor=tk.W, padx=12, pady=4, ipady=4)
        
        self.button_kirim = Button(self.pop_up_frame_content, text="Kirim", bg='#FFCC80', font=("Segoe UI Semibold", 10), command=self.submit_kategori)
        self.button_kirim.pack(ipadx=78, ipady=2, pady=16)

    def show_pop_up_filter(self):
        self.pop_up = Toplevel(self)
        list_kategori = self.get_list_kategori()
        list_kategori.append('')
        # list_kategori = ['Semua']
        # for kategori in self.get_list_kategori():
        #     list_kategori.append(kategori)

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = int(width / 2 - 300 / 2)
        y = int(height / 2 - 442 / 2 - 40)
        geometry = '300x442+' + str(x) + '+' + str(y)
        self.pop_up.geometry(geometry)
        self.pop_up.title("Filter")

        self.pop_up_frame = Frame(self.pop_up)
        self.pop_up_frame.pack(fill=tk.BOTH)

        self.label_title = Label(self.pop_up_frame, text = "Filter", font=("Segoe UI Semibold", 16), bg='#FFA000', fg='#263238')
        self.label_title.pack(ipady=10, fill=tk.X)
        
        self.pop_up_frame_content = Frame(self.pop_up)
        self.pop_up_frame_content.pack(padx=40, pady=8, fill=tk.BOTH)

        fields = {}
        fields['label_status'] = Label(self.pop_up_frame_content, text='Jenis Status :', font=("Segoe UI Semibold", 12))
        fields['entry_status'] = ttk.Combobox(self.pop_up_frame_content, values=['On Going', 'Done', 'Expired', ''], state='readonly', textvariable=self.INPUT_FILTER_STATUS, width= 40, font=("Segoe UI", 12))
        fields['label_rentang_waktu'] = Label(self.pop_up_frame_content, text='Rentang Waktu :', font=("Segoe UI Semibold", 12))
        fields['entry_rentang_waktu'] = ttk.Combobox(self.pop_up_frame_content, values=['Hari Ini', ''], state='readonly', textvariable=self.INPUT_FILTER_WAKTU, width= 40, font=("Segoe UI", 12))
        fields['label_kategori'] = Label(self.pop_up_frame_content, text='Kategori :', font=("Segoe UI Semibold", 12))
        fields['entry_kategori'] = ttk.Combobox(self.pop_up_frame_content, values=list_kategori, state='readonly', textvariable=self.INPUT_FILTER_KATEGORI, width= 40, font=("Segoe UI", 12))

        for field in fields.values():
            field.pack(anchor=tk.W, padx=12, pady=4, ipady=4)
        
        self.button_kirim = Button(self.pop_up_frame_content, text="Kirim", bg='#FFCC80', font=("Segoe UI Semibold", 10), command=self.submit_filter)
        self.button_kirim.pack(ipadx=78, ipady=2, pady=32)
    
    def get_list_kategori(self):
        datas = self.get_list_class_kategori()
        list_kategori = []
        for kategori in datas:
            list_kategori.append((kategori.nama))   
        return list_kategori

    def get_list_kegiatan(self, list_class_kegiatan):
        # datas = list_class_kegiatan
        list_kegiatan = []
        for kegiatan in list_class_kegiatan:
            list_kegiatan.append((kegiatan.id, kegiatan.nama, kegiatan.waktu, kegiatan.kategori, kegiatan.status))
        return list_kegiatan

    def get_list_class_kegiatan(self, list_data_kegiatan): # list data kegiatan hrs yg udah di append
        # list_data_kegiatan = Model.get_all_kegiatan_with_nama_kategori(self)
        list_class_kegiatan = []
        for kegiatan in list_data_kegiatan:
            list_class_kegiatan.append(Kegiatan(kegiatan[0], kegiatan[1], kegiatan[2], kegiatan[3], kegiatan[5]))
        return list_class_kegiatan

    def get_list_class_kategori(self):
        list_kategori = Model.get_all_kategori(self)
        list_class_kategori = []
        for kategori in list_kategori:
            list_class_kategori.append(Kategori(kategori[0], kategori[1]))
        return list_class_kategori
    
    def get_id_kategori_by_nama(self, nama):
        id = 0
        list_kategori = self.get_list_class_kategori()
        for kategori in list_kategori:
            if kategori.nama == nama:
                id = kategori.id
                break
        return id

    def submit_kegiatan(self):
        print("Kegiatan Submited")
        print(self.INPUT_NAMA_KEGIATAN.get())
        print(self.INPUT_BATAS_WAKTU.get())
        print(self.INPUT_KATEGORI.get())
        print(self.get_id_kategori_by_nama(self.INPUT_KATEGORI.get()))
        # try:
        if self.INPUT_NAMA_KEGIATAN.get() == "" or self.INPUT_BATAS_WAKTU.get() == "" or self.INPUT_KATEGORI.get() == "":
            messagebox.showerror("Error", "Oops, jangan lupa masukkan seluruh field")
        else:
            id = 0
            for i in range(0, len(self.get_list_class_kegiatan(Model.get_all_kegiatan_with_nama_kategori(self)))):
                if i == (len(self.get_list_class_kegiatan(Model.get_all_kegiatan_with_nama_kategori(self)))-1):
                    id = self.get_list_class_kegiatan(Model.get_all_kegiatan_with_nama_kategori(self))[i].id + 1
            print("IDD", id)
            # Update status expired
            date_time_obj = datetime.strptime(self.INPUT_BATAS_WAKTU.get(), '%Y-%m-%d')
            status = 'On Going'
            if (datetime.now().year > date_time_obj.year):
                status = 'Expired'
            elif (datetime.now().year == date_time_obj.year):
                if (datetime.now().month > date_time_obj.month):
                    status = 'Expired'
                elif (datetime.now().month == date_time_obj.month):
                    if (datetime.now().day > date_time_obj.day):
                        status = 'Expired'
                    else:
                        pass
            kegiatan = Kegiatan(id, self.INPUT_NAMA_KEGIATAN.get(), self.INPUT_BATAS_WAKTU.get(), status, self.get_id_kategori_by_nama(self.INPUT_KATEGORI.get()))
            Model.insert_kegiatan(self, kegiatan)
        # except:
            # messagebox.showerror("Error", "Error Occured")
        self.INPUT_NAMA_KEGIATAN.set("")
        self.INPUT_BATAS_WAKTU.set("")
        self.INPUT_KATEGORI.set("")
        self.pop_up.destroy()
        self.render_data_kegiatan_all()
        
    def submit_kategori(self):
        print("Kategori Submited")
        print(self.INPUT_NAMA_KATEGORI.get())
        try:
            if self.INPUT_NAMA_KATEGORI.get() == "" :
                messagebox.showerror("Error", "All fields are required")
            else:
                id = len(self.get_list_kategori()) + 1
                kategori = Kategori(id, self.INPUT_NAMA_KATEGORI.get())
                Model.insert_kategori(self, kategori)
        except:
            messagebox.showerror("Error", "Error Occured")
        self.INPUT_NAMA_KATEGORI.set("")
        self.pop_up.destroy()

    def delete_kegiatan(self):
        # Get the selected iid
        selected_item = self.tree.focus()
        id = self.tree.item(selected_item).get('values')[0]
        try:
            Model.remove_kegiatan_by_id(self, id)
        except:
            messagebox.showerror("Error", "Error Occured")
        self.render_data_kegiatan_all()
    
    def tandai_selesai_kegiatan(self):
        # Get the selected iid
        selected_item = self.tree.focus()
        id = self.tree.item(selected_item).get('values')[0]
        try:
            Model.update_status(self, id, 'Done')
        except:
            messagebox.showerror("Error", "Error Occured")
        self.render_data_kegiatan_all()

    def submit_filter(self):
        print("Filter Submited")
        print(self.INPUT_FILTER_STATUS.get())
        print(self.INPUT_FILTER_WAKTU.get())
        print(self.INPUT_FILTER_KATEGORI.get())
        print(self.get_id_kategori_by_nama(self.INPUT_FILTER_KATEGORI.get()))
        # try:
        if self.INPUT_FILTER_STATUS.get() != "":
            if self.INPUT_FILTER_KATEGORI.get() == "" and self.INPUT_FILTER_WAKTU.get() == "":
                self.render_data_kegiatan_filtered_status(self.INPUT_FILTER_STATUS.get())
            elif self.INPUT_FILTER_KATEGORI.get() != "" and self.INPUT_FILTER_WAKTU.get() == "":
                self.render_data_kegiatan_filtered_status_kategori(self.INPUT_FILTER_STATUS.get(), self.INPUT_FILTER_KATEGORI.get())
            elif self.INPUT_FILTER_KATEGORI.get() == "" and self.INPUT_FILTER_WAKTU.get() == "Hari Ini":
                self.render_data_kegiatan_filtered_status_today(self.INPUT_FILTER_STATUS.get())
            elif self.INPUT_FILTER_KATEGORI.get() != "" and self.INPUT_FILTER_WAKTU.get() == "Hari Ini":
                self.render_data_kegiatan_filtered_status_kategori_today(self.INPUT_FILTER_STATUS.get(), self.INPUT_FILTER_KATEGORI.get())
        elif self.INPUT_FILTER_STATUS.get() == "":
            if self.INPUT_FILTER_KATEGORI.get() != "" and self.INPUT_FILTER_WAKTU.get() == "":
                self.render_data_kegiatan_filtered_kategori(self.INPUT_FILTER_KATEGORI.get())
            elif self.INPUT_FILTER_KATEGORI.get() != "" and self.INPUT_FILTER_WAKTU.get() == "Hari Ini":
                self.render_data_kegiatan_filtered_kategori_today(self.INPUT_FILTER_KATEGORI.get())
            elif self.INPUT_FILTER_KATEGORI.get() == "" and self.INPUT_FILTER_WAKTU.get() == "Hari Ini":
                self.render_data_kegiatan_filtered_today()
            elif self.INPUT_BATAS_WAKTU.get() == "" and self.INPUT_FILTER_KATEGORI.get() == "":
                self.render_data_kegiatan_all()
        # except:
            # messagebox.showerror("Error", "Error Occured")
        self.INPUT_FILTER_STATUS.set("")
        self.INPUT_BATAS_WAKTU.set("")
        self.INPUT_FILTER_KATEGORI.set("")
        self.pop_up.destroy()
    
    def render_data_kegiatan_all(self):
        self.tree.delete(*self.tree.get_children())
        list_kegiatan = self.get_list_kegiatan(self.get_list_class_kegiatan(Model.get_all_kegiatan_with_nama_kategori(self)))
        # Add data to the treeview
        # print(list_kegiatan)
        for kegiatan in list_kegiatan:
            # Update status expired
            date_time_obj = datetime.strptime(kegiatan[2], '%Y-%m-%d')
            if (datetime.now().year > date_time_obj.year):
                Model.update_status(self, kegiatan[0], 'Expired')
            elif (datetime.now().year == date_time_obj.year):
                if (datetime.now().month > date_time_obj.month):
                    Model.update_status(self, kegiatan[0], 'Expired')
                elif (datetime.now().month == date_time_obj.month):
                    if (datetime.now().day > date_time_obj.day):
                        Model.update_status(self, kegiatan[0], 'Expired')
            # Show
            self.tree.insert('', tk.END, values=kegiatan)
    
    def render_data_kegiatan_filtered_today(self):
        self.tree.delete(*self.tree.get_children())
        list_class_kegiatan = self.get_list_kegiatan(self.get_list_class_kegiatan(Model.get_kegiatan_filtered_today(self)))
        # Add data to the treeview
        for kegiatan in list_class_kegiatan:
            self.tree.insert('', tk.END, values=kegiatan)
    
    def render_data_kegiatan_filtered_status(self, status):
        self.tree.delete(*self.tree.get_children())
        list_class_kegiatan = self.get_list_kegiatan(self.get_list_class_kegiatan(Model.get_kegiatan_filtered_status(self, status)))
        # Add data to the treeview
        for kegiatan in list_class_kegiatan:
            self.tree.insert('', tk.END, values=kegiatan)
    
    def render_data_kegiatan_filtered_kategori(self, kategori):
        self.tree.delete(*self.tree.get_children())
        list_class_kegiatan = self.get_list_kegiatan(self.get_list_class_kegiatan(Model.get_kegiatan_filtered_kategori(self, kategori)))
        # Add data to the treeview
        for kegiatan in list_class_kegiatan:
            self.tree.insert('', tk.END, values=kegiatan)
    
    def render_data_kegiatan_filtered_status_kategori(self, status, kategori):
        self.tree.delete(*self.tree.get_children())
        list_class_kegiatan = self.get_list_kegiatan(self.get_list_class_kegiatan(Model.get_kegiatan_filtered_status_kategori(self, status, kategori)))
        # Add data to the treeview
        for kegiatan in list_class_kegiatan:
            self.tree.insert('', tk.END, values=kegiatan)
    
    def render_data_kegiatan_filtered_status_today(self, status):
        self.tree.delete(*self.tree.get_children())
        list_class_kegiatan = self.get_list_kegiatan(self.get_list_class_kegiatan(Model.get_kegiatan_filtered_status_today(self, status)))
        # Add data to the treeview
        for kegiatan in list_class_kegiatan:
            self.tree.insert('', tk.END, values=kegiatan)
    
    def render_data_kegiatan_filtered_kategori_today(self, kategori):
        self.tree.delete(*self.tree.get_children())
        list_class_kegiatan = self.get_list_kegiatan(self.get_list_class_kegiatan(Model.get_kegiatan_filtered_kategori_today(self, kategori)))
        # Add data to the treeview
        for kegiatan in list_class_kegiatan:
            self.tree.insert('', tk.END, values=kegiatan)
    
    def render_data_kegiatan_filtered_status_kategori_today(self, status, kategori):
        self.tree.delete(*self.tree.get_children())
        list_class_kegiatan = self.get_list_kegiatan(self.get_list_class_kegiatan(Model.get_kegiatan_filtered_status_kategori_today(self, status, kategori)))
        # Add data to the treeview
        for kegiatan in list_class_kegiatan:
            self.tree.insert('', tk.END, values=kegiatan)
    
