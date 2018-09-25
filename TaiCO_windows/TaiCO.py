#!usr/bin/python3
# This file is covered by the LICENSE.txt file in the root of this project.

"""
Copyright (C) 2016  Author: Vasileios Rantos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For further information and support please contact author : vrantos@hotmail.gr

"""
import sys
import re
import string
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tkinter.messagebox
import os
import numpy as np

global root
global only_folder
infile1 = None
infile2 = None
infile3 = None
filename1 = ''
protein_fasta_filename = ''
filename3 = ''
file1 = ""
file2 = ""
file3 = ""



#pop up message when hitting biobuilders magic button
def magicbutton():
    #message box after the procedure was finished
    tkinter.messagebox.showinfo('TaiCO 2016', 'The DTU Igem team 2016 greets and strongly advises you to : KEEP CALM AND OPTIMIZE !!!')
    
#search file
def ask_for_file():
    return filedialog.askopenfilename(initialdir='Z:/')

#function for dictionaries with values only codons not codons+w values
def final_dict(random_dict):
    """Function to finalize dict"""
    for key,value in random_dict.items():
        random_dict[key] = value[0:3]
    return random_dict

#choose infile 1
def input_file1():
    #open the gcn file
    global filename1
    global infile1
    filename1=ask_for_file()
    infile1 = open(filename1, 'r')
    #show only real name of file
    global name_file1
    name_file1 = filename1.split('/')
    global file1
    global root
    file1 = Label(root, text=name_file1[-1],font=("Arial", 11),bg="white")
    file1.place(x=494,y=109)

#select file with sequences
def input_file2():
    #open the file with the sequences
    global protein_fasta_filename
    global infile2
    filename2=ask_for_file()
    infile2 = open(filename2, 'r')
    #show only real name of file
    name_file2 = filename2.split('/')
    global file2
    file2 = Label(root, text=name_file2[-1],font=("Arial", 11),bg="white")
    file2.place(x=494,y=169)

#check or not box to produce final result -> main analysis part
def input_file3():
    #open the file with the sequences
    global filename3
    global infile3
    filename3=ask_for_file()
    infile3 = open(filename3, 'r')
    #show only real name of file
    name_file3 = filename3.split('/')
    global file3
    file3 = Label(root, text=name_file3[-1],font=("Arial", 11),bg="white")
    file3.place(x=494,y=229)


def restart():
    if tkinter.messagebox.askokcancel("Back to Menu", "Sure you want to go back to Menu?"):
        root.destroy()
        import GUI
        GUI.create_main_window()

def main_script():
    #initialize dicts,lists,strings
    #opt_codon = first option
    #low_codon = second option
    #last_codon = third option
    #not_used_codon = fourth option
    #remaining = last option
    #restrictions options priotirized
    opt_codon = {}
    low_codon = {}
    last_codon = {}
    not_used_codon = {}
    #the remaining codons are not implemented in this script (feel free to elaborate it)
    remaining = []
    first_rem = []
    second_rem = []
    value_codon = ''
    value2_codon = ''
    value3_codon = ''
    value4_codon = ''
    (seq, head) = ('', '')
    protein_seq = []
    dna = ''
    head_list = []
    seq_opt = ''
    check = 0
    counter = 0
    res_sites = []
    final = []
    i = 0

    #variables, dicts and lists for tai calculation
    #define and calculate S matrix
    A = [1,0,0,0.0001]
    C = [0,1,0,0.72]
    G = [0.32,0,1,0]
    T = [0,0.59,0,1]
    smat = []
    smat.append(A)
    smat.append(C)
    smat.append(G)
    smat.append(T)
    #list with correct order of aa
    sort_aa = ["K","N","K","N","T","T","T","T","R","S","R","S","I","I","M","I","Q","H","Q","H","P","P","P","P","R","R","R","R","L","L","L","L","E","D","E","D","A","A","A","A","G","G","G","G","V","V","V","V","X","Y","X","Y","S","S","S","S","X","C","W","C","L","F","L","F"]
    #initialize lists,variables and open file
    trna_crap = []
    t_row = []
    trna_final = []
    high_w_mat = []
    w_list = []
    final_format = []
    anti_dict = {}
    rev_comp_dict = {}
    anti_codon = ''
    counter_codon = 0

    global infile1
    global infile2
    global infile3

    #in case the user fails to upload a file
    if infile1 == None or infile2 == None:
        #message box after the procedure was finished
        tkinter.messagebox.showinfo('TaiCO 2016', 'The analysis cannot start : table file or desired fasta file is/are missing !')
        return

    data = infile1.readlines()
    #put all 64 counts in a dict
    for i in range(1,len(data)):
        t_count = data[i].split()
        if t_count[0] not in anti_dict:
            anti_dict[t_count[0]] = float(t_count[1])       
    #reverse complement in a new dict
    for key,value in anti_dict.items():
        rev_comp = key[::-1]
        for letter in range(len(rev_comp)):
            if rev_comp[letter] == "A":
                anti_codon += "T"
            elif rev_comp[letter] == "T":
                anti_codon += "A"
            elif rev_comp[letter] == "G":
                anti_codon += "C"
            else:
                anti_codon += "G"
        rev_comp_dict[anti_codon] = value
        anti_codon = ''
    anti_codon = ''

    #save sorted keys and their values of dict to list
    key_list = sorted(rev_comp_dict.keys())
    for i in key_list:
        if i in rev_comp_dict:
            trna_crap.append(rev_comp_dict[i])

    #create matrix 16X4
    for num in trna_crap:
        t_row.append(num)
        if len(t_row) == 4:
            trna_final.append(t_row)
            t_row = []  
    trna_crap = []
    t_row = []

    #tranverse matrix -> 4X16
    trna_final = np.array(trna_final)
    trna_final = trna_final.T

    #matrix product
    x = np.matrix(smat)
    y = np.matrix(trna_final)
    trna_final = []
    w_crap = np.matrix(x*y)

    #flatten matrix to find highest W
    high_w_mat = (w_crap).ravel()
    highest_w = np.amax(high_w_mat)

    #update w_crap for 0 values (stop codons)
    #1)find the mean first from the w_crap matrix
    #2)replace all 0 with means
    mean_mat = w_crap.mean()
    w_crap[w_crap==0] = mean_mat

    #final matrix and file production with codons and w
    final_matrix = np.divide(w_crap,float(highest_w))
    final_matrix = final_matrix.T

    #write matrix to file
    final_matrix.tofile('temp_mat.txt',sep='\t')
    infile_mat = open('temp_mat.txt','r')
    infile1.close()

    #write final file
    codon_outfile = open("temp_codons.txt",'w')
    for line in infile_mat:
        col_mat = line.split()
        for i in col_mat:
            i = float(i)
            i = float("{0:.3f}".format(i))
            i = str(i)
            #all floats should have 3 decimans (in total 5 characters)
            if len(i) == 5:
                codon_outfile.write(key_list[counter_codon]+"\t"+str(i)+"\t"+sort_aa[counter_codon]+"\n")
            else:
                i = str(i)
                i = i + "0"*(5-len(i))
                codon_outfile.write(key_list[counter_codon]+"\t"+str(i)+"\t"+sort_aa[counter_codon]+"\n")
            counter_codon += 1
    counter_codon = 0
    rev_comp_dict = {}
    anti_dict = {}
    ###initialize all variables that have to be empty
    codon_outfile.close()
	
    #input final final
    infile_input = open("temp_codons.txt",'r')
        
    #construction of dictionaries with priority codons
    for line in infile_input:
        col = line.split()
        if col[2] not in opt_codon:
            opt_codon[col[2]] = col[0] + "," + str(col[1])
        elif col[2] in opt_codon:
            value_codon = opt_codon[col[2]]
            w = re.search('\,(\d+\.?\d+)',value_codon)
            num_weight = float(w.group(1))
            if col[2] not in low_codon:
                if float(col[1]) > num_weight:
                    opt_codon[col[2]] = col[0] + "," + str(col[1])
                    low_codon[col[2]] = value_codon
                else:
                    low_codon[col[2]] = col[0] + "," + str(col[1])
            else:
                value2_codon = low_codon[col[2]]
                w2 = re.search('\,(\d+\.?\d+)',value2_codon)
                num2_weight = float(w2.group(1))
                if col[2] not in last_codon:
                    if float(col[1]) > num_weight:
                        opt_codon[col[2]] = col[0] + "," + str(col[1])
                        low_codon[col[2]] = value_codon
                        last_codon[col[2]] = value2_codon
                    else:
                        if float(col[1]) > num2_weight:
                            low_codon[col[2]] = col[0] + "," + str(col[1])
                            last_codon[col[2]] = value2_codon
                        else:
                            last_codon[col[2]] = col[0] + "," + str(col[1])
                else:
                    value3_codon = last_codon[col[2]]
                    w3 = re.search('\,(\d+\.?\d+)',value3_codon)
                    num3_weight = float(w3.group(1))
                    if col[2] not in not_used_codon:
                        if float(col[1]) > num_weight:
                            opt_codon[col[2]] = col[0] + "," + str(col[1])
                            low_codon[col[2]] = value_codon
                            last_codon[col[2]] = value2_codon
                            not_used_codon[col[2]] = value3_codon
                        else:
                            if float(col[1]) > num2_weight:
                                low_codon[col[2]] = col[0] + "," + str(col[1])
                                last_codon[col[2]] = value2_codon
                                not_used_codon[col[2]] = value3_codon
                            else:
                                if float(col[1]) > num3_weight:
                                    last_codon[col[2]] = col[0] + "," + str(col[1])
                                    not_used_codon[col[2]] = value3_codon
                                else:
                                   not_used_codon[col[2]] = col[0] + "," + str(col[1])
                    else:
                        value4_codon = not_used_codon[col[2]]
                        w4 = re.search('\,(\d+\.?\d+)',value4_codon)
                        num4_weight = float(w4.group(1))
                        if float(col[1]) > num4_weight:
                          not_used_codon[col[2]] = col[0] + "," + str(col[1])
                          remaining.append(col[2] + ":" + value4_codon)
                        else:
                            remaining.append(col[2] + ":" + col[0] + "," + str(col[1]))
    col = ''
    
    #finalize dicts with the function above
    opt_codon = final_dict(opt_codon)
    low_codon = final_dict(low_codon)
    last_codon = final_dict(last_codon)
    not_used_codon = final_dict(not_used_codon)

    infile_input.close()
    os.remove("temp_codons.txt")

    #save all protein seqs and their heads to lists
    for line in infile2:
        if line.startswith(">"):
            if head != '':
                if seq[-1] is not "X":
                    seq += "X"
                seq = seq.upper()
                protein_seq.append(seq)
            head = line
            head_list.append(head[1:-1])
            seq = ''
        else:
            seq += line.strip()        
    if head != '':
        if seq[-1] is not "X":
            seq += "X"
        #save all protein seqs to a list
        seq = seq.upper()
        protein_seq.append(seq)
    seq = ''
    
    if infile3 is None:
        #start back-translating the protein sequences to the most optimized codons
        for i in protein_seq:
            for aa in i:
                if aa in opt_codon:
                    seq_opt += opt_codon[aa]
            final.append(seq_opt)
            seq_opt = ''
            
    elif infile3 is not None:
        #all restriction sites to one list
        for line in infile3:
            new_line = line.strip()
            new_line = new_line.upper()
            res_sites.append(new_line)

        #initialize iterator again coz was used above
        i = 0
        #now start building optimized DNA seqs with conditions
        for seq in protein_seq:
            for aa in range(len(seq)):
                if seq[aa] in opt_codon and dna == '':
                    dna += opt_codon[seq[aa]]
                else:
                    dna += opt_codon[seq[aa]]
                    while i <= len(res_sites)-1:
                        if res_sites[i] in dna and counter == 0:  
                            if seq[aa] in low_codon:
                                dna = dna[:-3] + low_codon[seq[aa]]
                                i = 0
                                counter += 1
                            elif seq[aa] not in low_codon and seq[aa-1] in low_codon:
                                dna = dna[:-6] + low_codon[seq[aa-1]] + opt_codon[seq[aa]]
                                i = 0
                                counter += 1
                            else:
                                dna = ''
                                i += 1
                        elif res_sites[i] in dna and counter == 1:
                            if seq[aa] in last_codon:
                                dna = dna[:-3] + last_codon[seq[aa]]
                                i = 0
                                counter += 1
                            elif seq[aa] not in last_codon and seq[aa-1] in low_codon:
                                dna = dna[:-6] + low_codon[seq[aa-1]] + opt_codon[seq[aa]]
                                i = 0
                                counter += 1
                            else:
                                dna = ''
                                i += 1
                        elif res_sites[i] in dna and counter == 2:
                            if seq[aa] in not_used_codon:
                                dna = dna[:-3] + not_used_codon[seq[aa]]
                                i = 0
                                counter += 1
                            elif seq[aa] not in not_used_codon and seq[aa-1] in low_codon:
                                dna = dna[:-6] + low_codon[seq[aa-1]] + opt_codon[seq[aa]]
                                i = 0
                                counter += 1
                            else:
                                dna = ''
                                i += 1
                        elif res_sites[i] in dna and counter == 3:
                            #iterate to save all remaining codons in a list
                            for rem_aa in remaining:
                                aa_splited = rem_aa.split(':')
                                if aa_splited[0] == seq[aa]:
                                    if first_rem == []:
                                        w1_splited = aa_splited[1].split(',')
                                        w1_final = float(w1_splited[1])
                                        first_rem.append(w1_splited[0])
                                    else:
                                        w2_splited = aa_splited[1].split(',')
                                        w2_final = float(w2_splited[1])
                                        if float(w2_final) < float(w1_final):
                                            second_rem.append(w2_splited[0])
                                        else:
                                            first_rem = []
                                            first_rem.append(w2_splited[0])
                                            second_rem.append(w1_splited[0])
                            if seq[aa] in first_rem:
                                dna = dna[:-3] + first_rem[0]
                                i = 0
                                counter += 1
                            elif seq[aa] not in first_rem and seq[aa-1] in low_codon:
                                dna = dna[:-6] + low_codon[seq[aa-1]] + opt_codon[seq[aa]]
                                i = 0
                                counter += 1
                            else:
                                dna = ''
                                i += 1
                        elif res_sites[i] in dna and counter == 4:
                            if seq[aa] in second_rem:
                                dna = dna[:-3] + first_rem[0]
                                i = 0
                                counter += 1
                            elif seq[aa] not in second_rem and seq[aa-1] in low_codon:
                                dna = dna[:-6] + low_codon[seq[aa-1]] + opt_codon[seq[aa]]
                                i = 0
                                counter += 1
                            else:
                                dna = ''
                                i += 1
                        elif res_sites[i] in dna and counter == 5:
                            if seq[aa-1] in low_codon:
                                dna = dna[:-6] + low_codon[seq[aa-1]] + opt_codon[seq[aa]]
                                i = 0
                                counter += 1
                            else:
                                dna = ''
                                i += 1
                        elif res_sites[i] in dna and counter == 6:
                            dna = ''
                            i += 1
                        elif res_sites[i] not in dna:
                            i += 1
                    i = 0
                    counter = 0
                    first_rem = []
                    second_rem = []
            seq_opt = dna
            if len(seq_opt) == 3*len(seq):
                final.append(seq_opt)
                seq_opt = ''
                dna = ''
                counter = 0
                i = 0
            else:
                final.append("No optimized sequence")
                seq_opt = ''
                dna = ''
                counter = 0
                i = 0

    global name_file1     
    #write final optimized sequences to file with fasta format
    outfile = open(name_file1[-1][:-4]+".fsa", 'w')
    for dna_seq in range(len(final)):
        outfile.write(">" + head_list[dna_seq]+"\n")
        for nucleotide in range(0,len(final[dna_seq]),60):
            outfile.write(final[dna_seq][nucleotide:nucleotide+60] + "\n")
            
    final = []       
    #inittialize in order to rerun if wanted
    infile1 = None
    infile2 = None
    infile3 = None
    outfile.close()

    #disappear file names
    global file1
    file1.place_forget()
    global file2
    file2.place_forget()
    global file3
    if file3 != '':
        file3.place_forget()
    global only_folder
    #message box after the procedure was finished
    tkinter.messagebox.showinfo('TaiCO 2016', 'File: '+name_file1[-1][:-4]+'.fsa\nsaved in folder: '+ only_folder[-1])

def run_taico():
    #create window
    global root
    root = Tk()
    root.configure(background='grey')
    root.geometry("700x422")
    root.resizable(width=False, height=False)
    root.title("TaiCO 2016 DTU")
    #shortcut image
    img = tkinter.Image("photo", file="logo.gif")
    root.tk.call('wm','iconphoto',root._w,img)

    #folder name to result file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    global only_folder
    only_folder = str(dir_path).split('/')

    #status bar
    status = Label(root,text="For help, please contact : vrantos@hotmail.gr",bd=2,relief=SUNKEN,anchor=W)
    status.pack(side=BOTTOM,fill=X)

    #rectangles wiht colours
    canvas = Canvas(root, width = 700, height = 422)
    canvas.pack()
    myrectangle1 = canvas.create_rectangle(0, 0, 700, 65, fill='black')
    canvas.itemconfig(myrectangle1, fill='#464444')
    myrectangle2 = canvas.create_rectangle(0, 0, 80, 422, fill='black')
    canvas.itemconfig(myrectangle2, fill='#141313')

    #gui name
    gui_name = Label(root, text="TaiCO",font=("Arial", 20,"bold"),bg="#464444",fg="white")
    gui_description = Label(root, text="- a tAI-based codon optimization tool",font=("Arial", 10,"bold"),bg="#464444",fg="white")
    gui_description.place(x=259,y=40)
    gui_name.place(x=339,y=8)

    #just to make my life easier with this files path (else no solvable)

    file1 = Label(root,bg="red")
    file2 = Label(root,bg="red")
    file3 = Label(root,bg="red")


    label_1 = Label(root, text="Upload species GCN table :", bg="white",font=("Arial",11),relief=RIDGE,borderwidth=3)
    label_2 = Label(root, text="Upload protein fasta file :", bg="white",font=("Arial",11),relief=RIDGE,borderwidth=3)
    label_3 = Label(root, text="Upload restriction sites file (optional) :", bg="white",font=("Arial",11),relief=RIDGE,borderwidth=3)

    button1 = Button(root, text="Search file", fg="black",bg="white", command=input_file1, relief=RAISED, borderwidth=3)
    button2 = Button(root, text="Search file", fg="black",bg="white", command=input_file2,relief=RAISED, borderwidth=3)
    button3 = Button(root, text="Search file", fg="black",bg="white", command=input_file3,relief=RAISED, borderwidth=3)
    start_button = Button(root, text="Start analysis", fg="black",bg="white", command=main_script,font=(15),relief=RAISED, borderwidth=3)
    back_button = Button(root, text="Back", fg="black",bg="white", command=restart,font=(15),relief=RAISED, borderwidth=3)

    # place widgets in window by coordinates
    button1.place(x=380,y=103)
    button2.place(x=380,y=163)
    button3.place(x=380,y=223)
    start_button.place(x=557,y=325)
    back_button.place(x=100,y=325)
    label_1.place(x=120,y=107)
    label_2.place(x=120,y=167)
    label_3.place(x=120,y=227)

    #emtpy (drawed) boxes for file names when selected
    myrectangle3 = canvas.create_rectangle(492, 106, 657, 133, fill='grey')
    canvas.itemconfig(myrectangle3, fill='white')
    myrectangle4 = canvas.create_rectangle(492, 166, 657, 193, fill='grey')
    canvas.itemconfig(myrectangle4, fill='white')
    myrectangle5 = canvas.create_rectangle(492, 226, 657, 253, fill='grey')
    canvas.itemconfig(myrectangle5, fill='white')

    #dna image
    dna_image = PhotoImage(file="dna.gif")
    dna_label1 = tkinter.Label(root,image=dna_image)
    dna_label1.place(x=160,y=327)

    #DTU Biobuilders image button
    photo = PhotoImage(file="logo.gif")

    Buttonimage=Button(root, image=photo,bg="white",command=magicbutton,relief=RAISED)
    Buttonimage.place(x=0,y=0)

    #ask before exit
    def Quit():
        if tkinter.messagebox.askokcancel("Quit", "Sure you want to QUIT?"):
            root.destroy()
    root.protocol("WM_DELETE_WINDOW", Quit)
    #continue running window
    root.mainloop()

if __name__ == '__main__':
    run_taico()