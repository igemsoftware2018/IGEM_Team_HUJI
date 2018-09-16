from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog
from tkfilebrowser import askopenfilename
import os
import webbrowser
global Fasta_File_name
global csv_file_name
global restriction_file_name


def run_optimization():
    from CodonOptimization import Main
    global protein_fasta_filename
    codon_usage_tables_filnames_list = []
    protein_fasta_filename = protein_fasta_filename
    ouput_file_location = ""
    Main.main(protein_fasta_filename=protein_fasta_filename,
              list_codon_usage_filenames=codon_usage_tables_filnames_list, output_destination=ouput_file_location)

protein_fasta_filename = ""
filename3 = ""
def run_Taico():
    from TaiCO_windows import TaiCO
    return

def problem():
    print("var does not get assigned a value")

def open_hebrew_u_website():
    webbrowser.open("http://2018.igem.org/Team:HebrewU")
def open_DTU_website():
    webbrowser.open("http://2016.igem.org/Team:DTU-Denmark")

def create_main_window():
    #create window

    root = Tk()

    v = tk.IntVar()
    root.configure(background='grey')
    root.geometry("700x422")
    root.resizable(width=False, height=False)
    root.title("MulTaiCO 2018 HebrewU (and DTU)")

    #status bar
    status = Label(root,text="For help, please contact : HujiGEM@gmail.com",bd=2,relief=SUNKEN,anchor=W)
    status.pack(side=BOTTOM,fill=X)

    #rectangles wiht colours
    canvas = Canvas(root, width = 700, height = 422)
    canvas.pack()
    myrectangle1 = canvas.create_rectangle(0, 0, 700, 65, fill='black')
    canvas.itemconfig(myrectangle1, fill='#464444')

    #gui name
    gui_Mul = Label(root, text="Mul",font=("Calibri", 23),bg="#464444",fg="green")
    gui_T = Label(root, text="T",font=("Calibri", 23, "bold"),bg="#464444",fg="white")
    gui_aiCO = Label(root, text="aiCO",font=("Calibri", 23),bg="#464444",fg="red")
    gui_Optimizeby = Label(root, text="Optimize by:",font=("Calibri", 15),fg="black")

    #Radio Buttons
    var = IntVar()
    var.set(1)

    Radio1 = Radiobutton(root, text="MulT (Multiple organism optimization by tRNA freq)",font=("Calibri", 15), variable=var,value=1, fg="#464444")
    Radio2 = Radiobutton(root, text="TaiCO (Single optimization by tAI)",font=("Calibri", 15), variable=var, value=2, fg="#464444" )


    def run_option():
        root.destroy()

        if var.get() == 1:
            create_Hebrew_U_window()
        elif var.get() == 2:
            run_Taico()

        else:
            problem()

    #next button
    Screen1_next = tk.Button(root,text="Next",font=("Calibri", 15) , command = run_option )

    #DTU logo
    photo_DTU = PhotoImage(file="DTU.gif")
    Buttonimage=Button(root, image=photo_DTU,bg="white",relief=RAISED,command = open_DTU_website)
    Buttonimage.place(x=620,y=350)


    #HebrewU logo
    photo_HebrewU = PhotoImage(file="HebrewU.gif")
    Buttonimage=Button(root, image=photo_HebrewU,bg="white",relief=RAISED, command = open_hebrew_u_website)
    Buttonimage.place(x=0,y=370)

    gui_description = Label(root, text="Multi-functional optimization tool",font=("Calibri", 12),bg="#464444",fg="white")

    gui_description.place(x=238,y=40)
    gui_Mul.place(x=283,y=4)
    gui_T.place(x=335,y=4)
    gui_aiCO.place(x=351,y=4)
    gui_Optimizeby.place(x=100,y=100)
    Radio1.place(x=150, y=150)
    Radio2.place(x=150, y=200)
    Screen1_next.place(x=500, y=275)
    root.mainloop()


#-------------------------------HebrewU 1 window------------------------------------------
def create_Hebrew_U_window():
    root2 = Tk()
    v = tk.IntVar()
    root2.configure(background='#00B2B2')
    root2.geometry("700x422")
    root2.resizable(width=False, height=False)
    root2.title("MulTaiCO 2018 HebrewU (and DTU)")


    #rectangles wiht colours
    canvas = Canvas(root2, width = 700, height = 422)
    canvas.pack()
    myrectangle1 = canvas.create_rectangle(0, 0, 700, 65, fill='black')
    canvas.itemconfig(myrectangle1, fill='#00B2B2')

    #gui name
    gui_MulT = Label(root2, text="MulT",font=("Calibri", 23),bg="#00B2B2",fg="white")
    gui_descriptio_MulT = Label(root2, text="Multiple organism optimization by tRNA freq",font=("Calibri", 12),bg="#00B2B2",fg="white")


    def get_fasta_file():
        global Fasta_File_name
        Fasta_File_name = askopenfilename(parent=root2, initialdir='Z:/')
    def get_restriction():
        global restriction_file_name
        restriction_file_name = askopenfilename()
    #Buttons and labels for protein and restriction inputs
    button2 = Button(root2, text="Search file", fg="black",bg="white",  borderwidth=3, command =get_fasta_file )
    button3 = Button(root2, text="Search file", fg="black",bg="white",  borderwidth=3, command = get_restriction)
    label_2 = Label(root2, text="Upload protein fasta file :", bg="#F0F0F0",font=("calibri",11))
    label_3 = Label(root2, text="Upload restriction sites file (optional) :", bg="#F0F0F0",font=("calibri",11))

    def get_back_to_main1():
        root2.destroy()
        create_main_window()

    def second_menu():
        global protein_fasta_filename
        global filename3
        if protein_fasta_filename == "" or protein_fasta_filename.split(".")[-1]!= "fasta":
            messagebox.showinfo('MulT 2018',
                                'Please select a FASTA file')
            return

        if not os.path.exists(protein_fasta_filename) :
            messagebox.showinfo('MulT 2018',
                                     'Invalid or unexisting FASTA file, please select another')
            return
        if not os.path.exists(filename3) and filename3 != "" :
             messagebox.showinfo('MulT 2018',"Non- existing restriction file. ")
             return
        root2.destroy()
        create_second_hebrew_U_window()


    #next button
    Screen1_next2 = tk.Button(root2,text="Next",font=("Calibri", 15 ), command =second_menu )
    #back_button
    Screen1_next = tk.Button(root2,text="Back",font=("Calibri", 15) , command = get_back_to_main1 )


    protein_fasta_filename = ''
    filename3 = ''
    file2 = Label(root2, bg="red")
    file3 = Label(root2, bg="red")

    # search file
    def ask_for_file():
        return filedialog.askopenfilename(initialdir='Z:/')

    # choose infile 1
    def input_file1():
        # open the gcn file
        global filename1
        filename1 = ask_for_file()
        # show only real name of file
        name_file1 = filename1.split('/')
        global file1
        file1 = Label(root2, text=name_file1[-1], font=("Arial", 11), bg="white")
        file1.place(x=494, y=109)

    # select file with sequences
    def input_file2():
        # open the file with the sequences
        global protein_fasta_filename
        protein_fasta_filename = ask_for_file()
        # show only real name of file
        name_file2 = protein_fasta_filename.split('/')
        global file2
        file2 = Label(root2, text=name_file2[-1], font=("Arial", 11), bg="white")
        file2.place(x=494, y=169)

    # check or not box to produce final result -> main analysis part
    def input_file3():
        # open the file with the sequences
        global filename3
        filename3 = ask_for_file()
        # show only real name of file
        name_file3 = filename3.split('/')
        global file3
        file3 = Label(root2, text=name_file3[-1], font=("Arial", 11), bg="white")
        file3.place(x=494, y=229)


    button2 = Button(root2, text="Search file", fg="black", bg="white", command=input_file2, relief=RAISED,
                     borderwidth=3)
    button3 = Button(root2, text="Search file", fg="black", bg="white", command=input_file3, relief=RAISED,
                     borderwidth=3)
    # place widgets in window by coordinates
    button2.place(x=380, y=163)
    button3.place(x=380, y=223)
    label_2.place(x=120, y=167)
    label_3.place(x=120, y=227)

    # emtpy (drawed) boxes for file names when selected
    myrectangle4 = canvas.create_rectangle(492, 166, 657, 193, fill='grey')
    canvas.itemconfig(myrectangle4, fill='white')
    myrectangle5 = canvas.create_rectangle(492, 226, 657, 253, fill='grey')
    canvas.itemconfig(myrectangle5, fill='white')
    button2.place(x=380,y=163)
    button3.place(x=380,y=223)
    label_2.place(x=100,y=167)
    label_3.place(x=100,y=227)
    Screen1_next2.place(x=600,y=325)
    Screen1_next.place(x = 100, y = 325)


    gui_MulT.place(x=320,y=4)
    gui_descriptio_MulT.place(x=210,y=40)
    root2.mainloop()



#-------------------------------HebrewU 2 window------------------------------------------
def create_second_hebrew_U_window():
    print("created")
    root3 = Tk()
    v = tk.IntVar()
    root3.configure(background='#00B2B2')
    root3.geometry("700x422")
    root3.resizable(width=False, height=False)
    root3.title("MulTaiCO 2018 HebrewU (and DTU)")


    #rectangles wiht colours
    canvas = Canvas(root3, width = 700, height = 422)
    canvas.pack()
    myrectangle1 = canvas.create_rectangle(0, 0, 700, 65, fill='black')
    canvas.itemconfig(myrectangle1, fill='#00B2B2')

    #gui name
    gui_MulT4 = Label(root3, text="MulT",font=("Calibri", 23),bg="#00B2B2",fg="white")
    gui_descriptio_MulT4 = Label(root3, text="Multiple organism optimization by tRNA freq",font=("Calibri", 12),bg="#00B2B2",fg="white")

    #Buttons and labels for more and optimizze buttons
    button_more = Button(root3, text="Add more organisms", bg="#F0F0F0",font=("calibri",15))
    label_compatible = Label(root3, text="Compatible organisms (by priority):", bg="#F0F0F0",font=("calibri",15))
    label_1 = Label(root3, text="1.", bg="#F0F0F0",font=("calibri",15))
    label_2 = Label(root3, text="2.", bg="#F0F0F0",font=("calibri",15))



    #next button
    Screen3_Optimize = tk.Button(root3,text="Optimize",font=("Calibri", 15) , command =run_optimization )


    button_more.place(x=100,y=350)
    label_compatible.place(x=210,y=100)
    label_1.place(x=100,y=150)
    label_2.place(x=100,y=202)
    Screen3_Optimize.place(x=500,y=350)


    #list1
    variable = StringVar(root3)
    variable.set("First pick") # default value
    w = OptionMenu(root3, variable, "Arabidopsis thaliana", "Saccharomyces cerevisiae", "homosapiens", "Escherichia coli")
    w.place(x=130,y=150)

    #list2
    variable = StringVar(root3)
    variable.set("Second pick") # default value
    w = OptionMenu(root3, variable, "Arabidopsis thaliana", "Saccharomyces cerevisiae", "homosapiens", "Escherichia coli")
    w.place(x=130,y=200)



    gui_MulT4.place(x=320,y=4)
    gui_descriptio_MulT4.place(x=210,y=40)



create_main_window()








