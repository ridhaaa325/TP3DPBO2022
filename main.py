from tkinter import *
import mysql.connector
from tkinter import ttk
from PIL import ImageTk, Image

# koneksi ke database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")

# fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result

# window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
   
    # Input 1 - Nama
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=50)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    # Input 2 - NIM
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=50) 
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    #input 3 - Gender 
    input_gender = StringVar()
    input_gender.set("Pria")
    label3 = Label(dframe, text="Gender").grid(row=2, column=0, sticky="w")
    Radiobutton(dframe, text="Pria", variable=input_gender, value="Pria").place(x=110,y=80)
    Radiobutton(dframe, text="Wanita", variable=input_gender, value="Wanita").place(x=200,y=80)

     # input 4 - Hobi
    options = [
        "Rebahan", 
        "Tiduran", 
        "Main game", 
        "Belajar",
        "Ngoding", 
        "Ngaji"
    ]
    label4 = Label(dframe, text="Hobi").grid(row=3, column=0, sticky="w")
    input_hobi = ttk.Combobox(dframe, value=options)
    input_hobi.current(0)
    input_hobi.grid(row=3, column=1, padx=20, pady=10, sticky='w')

    # Input 5 - Jurusan
    options = [
        "Filsafat Meme", 
        "Sastra Mesin", 
        "Teknik Kedokteran", 
        "Pendidikan Gaming"
    ]
    input_jurusan = StringVar(root) 
    input_jurusan.set(options[0])
    label5 = Label(dframe, text="Jurusan").grid(row=4, column=0, sticky="w")
    input5 = OptionMenu(dframe, input_jurusan, *options)
    input5.grid(row=4, column=1, padx=20, pady=10, sticky='w')

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_gender, input_hobi, input_jurusan), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

# untuk memasukan data
def insertData(parent, nama, nim, gender, hobi, jurusan):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    gender = gender.get()
    hobi = hobi.get()
    jurusan = jurusan.get()

    # kondisi jika ada inputan yang masih kosong
    if len(nama) == 0 or len(nim) == 0 or len(gender) == 0 or len(hobi) == 0 or len(jurusan) == 0:
        btn_ok = Button(top, text="Masih ada form yang kosong!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
    # jika inputan terisi semua, data akan diinput ke database
    else:
        sql = "INSERT INTO mahasiswa (nim, nama, gender, hobi, jurusan) VALUES (%s, %s, %s, %s, %s)"
        val = (nim, nama, gender, hobi, jurusan)
        dbcursor.execute(sql, val)
        mydb.commit()

        # jika data berhasil masuk ke database
        if(dbcursor.rowcount == 1): 
            # label5 = Label(dframe, text="Jurusan").grid(row=4, column=0, sticky="w")
            Label(top, text="Record inserted!").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        # jika data gagal masuk ke database
        else: 
            Label(top, text="Failed to insert data!").grid(row=0, column=0, padx=20, pady=10, sticky="w")
        # Input data disini
        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
  
# window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()

    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Gender", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# untuk foto fasilitas kampus
def images():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas Kampus")

    img1 = ImageTk.PhotoImage(Image.open('images/labkomputer.jpeg'))
    img2 = ImageTk.PhotoImage(Image.open('images/labmultimedia.jpeg'))
    img3 = ImageTk.PhotoImage(Image.open('images/learningspace.jpeg'))
    img4 = ImageTk.PhotoImage(Image.open('images/ruangkelas.jpg'))

    image_list = [img1, img2, img3, img4]

    frame = LabelFrame(top, borderwidth=0)
    frame.pack(padx=20, pady=20)

    label = Label(frame, text="Lab Komputer", bd=1, relief=SUNKEN, anchor=S)

    my_label = Label(frame, image=img1)
    my_label.grid(row=0, column=0, columnspan=3)

    # untuk next photo
    def forward(image_number): 
        nonlocal my_label
        nonlocal button_forward
        nonlocal button_back

        my_label.grid_forget() 
        my_label = Label(frame, image=image_list[image_number - 1])
        button_forward = Button(frame, text=">", command=lambda: forward(image_number + 1))
        button_back = Button(frame, text="<", command=lambda: back(image_number - 1))

        if image_number == 4:
            button_forward = Button(frame, text="Next", state=DISABLED) 

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_forward.grid(row=1, column=2)

    # untuk previous photo
    def back(image_number): 
        nonlocal my_label
        nonlocal button_forward
        nonlocal button_back

        my_label.grid_forget()  
        my_label = Label(frame, image=image_list[image_number - 1])
        button_forward = Button(frame, text=">", command=lambda: forward(image_number + 1))
        button_back = Button(frame, text="<", command=lambda: back(image_number - 1))

        if image_number == 1:
            button_back = Button(frame, text="Back", state=DISABLED) 

        my_label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_forward.grid(row=1, column=2)
    
    button_back = Button(frame, text="<", command=lambda: back(), state=DISABLED)
    button_exit = Button(frame, text="Exit Program", command=root.quit)
    button_forward = Button(frame, text=">", command=lambda: forward(2))

    button_back.grid(row=1, column=0)
    button_exit.grid(row=1, column=1)
    button_forward.grid(row=1, column=2, pady=10)

# hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)

    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)

    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

# hapus semua data
def delAll():
    top = Toplevel()

    sql = "DELETE FROM mahasiswa"
    dbcursor.execute(sql)
    mydb.commit()

    countData = dbcursor.rowcount

    if(countData > 0): 
        Label(top, text="Data deleted succesfully!").grid(row=0, column=0, padx=20, pady=10, sticky="w")
    else: 
        Label(top, text="Failed to delete data!").grid(row=0, column=0, padx=20, pady=10, sticky="w")

    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)


# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# facility btn
b_clear = Button(buttonGroup, text="Fasilitas Kampus", command=images, width=30)
b_clear.grid(row=2, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()