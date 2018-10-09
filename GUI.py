import threading
from tkinter import *
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys #.path import append as append_system_path
import webbrowser

#global variables
DEFULT_ENTRY_CSV_MSG = "Enter .csv file"
Fasta_File_name = ""
csv_file_name = ""
restriction_file_name = ""
ouput_file_location = ""
# 3rd option not shown.
is_3_shown = False
protein_fasta_filename = ""
fasta_file_name = ""
codon_usage_tables_filnames_list = []

def run_Taico():
    """
    runs the TaiCo optimization program
    :return:
    """
    from TaiCO_windows import TaiCO
    TaiCO.run_taico()
    return

def open_hebrew_u_website():
    """
    prints the official iGEM website for Hebrew U
    :return:
    """
    webbrowser.open("http://2018.igem.org/Team:HebrewU")
def open_DTU_website():
    """
    prints the official iGEM website for DTU
    :return:
    """
    webbrowser.open("http://2016.igem.org/Team:DTU-Denmark")

def create_main_window():
    """
    creates and runs the main loop for the tool selection screen.
    :return:
    """
    #create window
    root = Tk()
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
        """
        the function choosing which program to activate
        :return:
        """
        root.destroy()
        if var.get() == 1:
            create_Hebrew_U_window()
        elif var.get() == 2:
            run_Taico()


    #next button
    Screen1_next = tk.Button(root,text="Next",font=("Calibri", 15) , command = run_option )

    #DTU logo
    photo_DTU = PhotoImage(file="CodonOptimization/DTU.gif")
    Buttonimage=Button(root, image=photo_DTU,bg="white",relief=RAISED,command = open_DTU_website)
    Buttonimage.place(x=620,y=350)


    #HebrewU logo
    photo_HebrewU = PhotoImage(file="CodonOptimization/HebrewU.gif")
    Buttonimage=Button(root, image=photo_HebrewU,bg="white",relief=RAISED, command = open_hebrew_u_website)
    Buttonimage.place(x=0,y=370)

    gui_description = Label(root, text="Multi-functional optimization tool",font=("Calibri", 12),bg="#464444",fg="white")
    #placing
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
    """
    creates and runs the main loop for the first screen of the MOOLTI tool.
    :return:
    """
    root2 = Tk()
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
    #create labels
    fasta_label = Label(root2, text="Upload protein fasta file :", bg="#F0F0F0",font=("calibri",11))
    restriction_label = Label(root2, text="Upload restriction sites file (optional) :", bg="#F0F0F0",font=("calibri",11))
    destination_label = Label(root2, text="Enter destination Folder:", bg="#F0F0F0",font=("calibri",11))

    def get_back_to_main1():
        """
        destroys the current screen and returns to previous screen.
        :return:
        """
        root2.destroy()
        create_main_window()

    def second_menu():
        """
        validates input, continues to second menu
        :return:
        """
        global restriction_file_name
        global ouput_file_location
        global protein_fasta_filename
        global fasta_file_name

        restriction_file_name = restriction_entry.get()
        protein_fasta_filename = fasta_entry.get()
        ouput_file_location = output_entry.get()
        if protein_fasta_filename == "" or protein_fasta_filename.split(".")[-1]!= "fasta":
            messagebox.showinfo('MulT 2018',
                                'Please select a FASTA file')
            return

        if not os.path.exists(protein_fasta_filename) :
            messagebox.showinfo('MulT 2018',
                                     'Invalid or unexisting FASTA file, please select another')
            return
        if not os.path.exists(protein_fasta_filename) and protein_fasta_filename != "" :
             messagebox.showinfo('MulT 2018',"Non- existing restriction file. ")
             return
        root2.destroy()
        create_second_hebrew_U_window()


    #next button
    Screen1_next2 = tk.Button(root2,text="Next",font=("Calibri", 15 ), command =second_menu )
    #back_button
    screen1_back = tk.Button(root2,text="Back",font=("Calibri", 15) , command = get_back_to_main1 )
    #creates entrys
    output_entry = Entry(root2)
    fasta_entry = Entry(root2)
    restriction_entry = Entry(root2)

    global ouput_file_location
    global protein_fasta_filename
    global restriction_file_name
    #makes sure the value isn't lost between screens
    fasta_entry.insert(0, protein_fasta_filename)
    restriction_entry.insert(0, restriction_file_name)
    output_entry.insert(0, ouput_file_location)

    # select file with sequences
    def input_file2():
        """
        inserts the input into the fasta variable
        :return:
        """
        # open the file with the sequences
        global protein_fasta_filename
        if protein_fasta_filename != "":
            fasta_entry.delete(0, END)
        protein_fasta_filename = filedialog.askopenfilename()
        fasta_entry.insert(0, protein_fasta_filename)

    def input_file3():
        # open the file with the sequences
        global restriction_file_name
        if restriction_file_name != "":
            restriction_entry.delete(0, END)
        messagebox.showinfo('MOOTI 2018',
                            'Please enter a text file containing restriction enzymes names, sperated by a comma.'
                            ' for example:\n EcoRI,HindIII,BamHI \n It\'s case sensitive !')

        restriction_file_name = filedialog.askopenfilename()
        with open(restriction_file_name, 'r') as content_file:
             content = content_file.read()
        restriction_entry.insert(0, content)

    def output_file():
        """
        saves the ouput file location
        :return:
        """
        # open the file with the sequences
        global ouput_file_location
        if ouput_file_location != "":
            output_entry.delete(0, END)
        ouput_file_location = filedialog.askopenfilename()
        #show in entry
        output_entry.insert(0, ouput_file_location)

    #create buttons
    fasta_search_button = Button(root2, text="Search file", fg="black", bg="white", command=input_file2, relief=RAISED,
                     borderwidth=3)
    search_restriction_button = Button(root2, text="Search file", fg="black", bg="white", command=input_file3, relief=RAISED,
                     borderwidth=3)
    output_search_button = Button(root2, text="Select folder", fg="black", bg="white", command=output_file, relief=RAISED,
                     borderwidth=3)

    # place buttons in window by coordinates
    fasta_search_button.place(x=380, y=163)
    output_search_button.place(x=380, y=223)
    search_restriction_button.place(x = 380, y = 280)
    Screen1_next2.place(x=600,y=325)
    screen1_back.place(x = 100, y = 325)

    #place entrys
    fasta_entry.place(x = 480, y = 167)
    output_entry.place(x = 480, y = 225)
    restriction_entry.place(x = 480, y = 280)
    #place labels
    fasta_label.place(x=100,y=167)
    destination_label.place(x=100,y=227)
    restriction_label.place(x=100, y=277)

    ouput_file_location = output_entry.get()
    global restriction_file_name
    restriction_file_name = restriction_entry.get()

    gui_MulT.place(x=320,y=4)
    gui_descriptio_MulT.place(x=210,y=40)
    root2.mainloop()


#-------------------------------HebrewU 2 window------------------------------------------
def create_second_hebrew_U_window():
    """
    creates and runs the main loop for the first screen of the MOOLTI tool.
    :return:
    """
    root3 = Tk()
    root3.configure(background='#00B2B2')
    root3.geometry("700x422")
    root3.resizable(width=False, height=False)
    root3.title("MulTaiCO 2018 HebrewU (and DTU)")

    global codon_usage_tables_filnames_list
    def get_back_to_second_window():
        """
        closes the current screen and proceedes to the second menu
        :return:
        """
        root3.destroy()
        create_Hebrew_U_window()


    #rectangles wiht colours
    canvas = Canvas(root3, width = 700, height = 422)
    canvas.pack()
    myrectangle1 = canvas.create_rectangle(0, 0, 700, 65, fill='black')
    canvas.itemconfig(myrectangle1, fill='#00B2B2')

    #gui name
    gui_MulT4 = Label(root3, text="MulT", font=("Calibri", 23), bg="#00B2B2", fg="white")
    gui_descriptio_MulT4 = Label(root3, text="Multiple organism optimization by tRNA freq",font=("Calibri", 12),bg="#00B2B2",fg="white")

    # select file with sequences
    def input_file(v):
        """
        a generalized input function
        :param v: the entry variable to fill
        :return:
        """
        # open the file with the sequences
        v.delete(0,END)
        v.insert(0, filedialog.askopenfilename())

    # Buttons and labels for more and optimizze buttons
    def addmore():
        """
        shows one or two more buttons
        :return:
        """
        global is_3_shown
        if is_3_shown == False:
            label_3.place(x=100, y=244)
            v3.place(x=430, y=244)
            third_organism_button.place(x=340, y=244)
            is_3_shown = True

        else:
            label_4.place(x=100, y=296)
            v4.place(x=430, y=296)
            fourth_organism_button.place(x=340, y=296)


    #Buttons and labels for more and optimizze buttons
    button_more = Button(root3, text="Add more organisms", bg="#F0F0F0", font=("calibri", 15), command=addmore)
    button_back = Button(root3, text="Back", bg="#F0F0F0", font=("calibri", 15), command=get_back_to_second_window)
    first_organism_button = Button(root3, text="Search file", fg="black", bg="white", command=lambda: input_file(v1), relief=RAISED,
                                 borderwidth=3)
    second_organism_button = Button(root3, text="Search file", fg="black", bg="white", command=lambda: input_file(v2),
                                       relief=RAISED,
                                       borderwidth=3)
    third_organism_button = Button(root3, text="Search file", fg="black", bg="white", command=lambda: input_file(v3),
                                  relief=RAISED,
                                  borderwidth=3)
    fourth_organism_button = Button(root3, text="Search file", fg="black", bg="white", command=lambda: input_file(v4),
                                   relief=RAISED,
                                   borderwidth=3)

    #create labels
    label_compatible = Label(root3, text="Compatible organisms :", bg="#F0F0F0", font=("calibri", 15))
    label_1 = Label(root3, text="Add organism codon usage table file:", bg="#F0F0F0", font=("calibri", 11))
    label_2 = Label(root3, text="Add organism codon usage table file:", bg="#F0F0F0", font=("calibri", 11))
    label_3 = Label(root3, text="Add organism codon usage table file:", bg="#F0F0F0", font=("calibri", 11))
    label_4 = Label(root3, text="Add organism codon usage table file:", bg="#F0F0F0", font=("calibri", 11))
    #placements
    button_back.place(x = 100, y = 350)
    button_more.place(x=230, y=350)
    first_organism_button.place(x=340, y=140)
    second_organism_button.place(x=340, y=192)
    label_compatible.place(x=100, y=100)
    label_1.place(x=100, y=140)
    label_2.place(x=100, y=192)

    #first organizm
    v1 = Entry(root3)
    v1.insert(0,DEFULT_ENTRY_CSV_MSG)  # default value
    v1.place(x=430, y=140)
    #second organizm
    v2 = Entry(root3)
    v2.insert(0, DEFULT_ENTRY_CSV_MSG)  # default value
    v2.place(x=430, y=192)

    # 3rd organizm
    v3 = Entry(root3)
    v3.insert(0, DEFULT_ENTRY_CSV_MSG)
    # 4th organizm
    v4 = Entry(root3)
    v4.insert(0, DEFULT_ENTRY_CSV_MSG)

    boolvar = IntVar()
    boolvar.set(3)

    def run_optimization():
        """
        uses user input to run the MOOLTI Codon Optimization
        :return:
        """
        sys.path.append(os.path.join(sys.path[0], "CodonOptimization"))
        import Main
        global protein_fasta_filename
        name1 =  v1.get()
        name2 =  v1.get()
        name3 =  v1.get()
        name4 =  v1.get()
        codon_usage_tables_filnames_list = []
        if name1 != DEFULT_ENTRY_CSV_MSG:
            codon_usage_tables_filnames_list.append(name1)

        if name2 != DEFULT_ENTRY_CSV_MSG:
            codon_usage_tables_filnames_list.append(name2)
        if name3 != DEFULT_ENTRY_CSV_MSG:
            codon_usage_tables_filnames_list.append(name3)
        if name4 != DEFULT_ENTRY_CSV_MSG:
            codon_usage_tables_filnames_list.append(name4)
        protein_fasta_filename = protein_fasta_filename
        global ouput_file_location
        global restriction_file_name

        opened_files = [open(filename, "r") for filename in codon_usage_tables_filnames_list]
        with open(protein_fasta_filename, mode = "r") as opened_fasta_file, open(ouput_file_location, 'w') as opened_output_file:

            return Main.main(protein_fasta_open_file=opened_fasta_file,
                             list_codon_usage_open_files=opened_files,
                             output_destination=opened_output_file,restriction_enzymes = restriction_file_name )

    def handle_click():
        """
        handles the button click, and the sucsess or failure of the Codon optimization function
        :return:
        """

        Message = run_optimization()

        messagebox.showinfo('MulT 2018', Message)
        root3.destroy()
        create_main_window()


    Screen3_Optimize = Button(root3, text="Optimize", font=("Calibri", 15), command=handle_click)
    Screen3_Optimize.place(x=500, y=350)


    gui_MulT4.place(x=320,y=4)
    gui_descriptio_MulT4.place(x=210,y=40)

    root3.mainloop()

if __name__ == '__main__':

    create_main_window()
