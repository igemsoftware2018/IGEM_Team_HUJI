from tkinter import *
import tkinter as tk

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
Radio1 = Radiobutton(root, text="MulT (Multiple organism optimization by tRNA freq)",font=("Calibri", 15), variable=v,value=1, fg="#464444")
Radio2 = Radiobutton(root, text="TaiCO (Single optimization by tAI)",font=("Calibri", 15), variable=v, value=2, fg="#464444")

#next button
Screen1_next = tk.Button(root,text="Next",font=("Calibri", 15))

#DTU logo
photo_DTU = PhotoImage(file="DTU.gif")
Buttonimage=Button(root, image=photo_DTU,bg="white",relief=RAISED)
Buttonimage.place(x=620,y=350)


#HebrewU logo
photo_HebrewU = PhotoImage(file="HebrewU.gif")
Buttonimage=Button(root, image=photo_HebrewU,bg="white",relief=RAISED)
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



#-------------------------------HebrewU 1 window------------------------------------------
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

#Buttons and labels for protein and restriction inputs
button2 = Button(root2, text="Search file", fg="black",bg="white",  borderwidth=3)
button3 = Button(root2, text="Search file", fg="black",bg="white",  borderwidth=3)
label_2 = Label(root2, text="Upload protein fasta file :", bg="#F0F0F0",font=("calibri",11))
label_3 = Label(root2, text="Upload restriction sites file (optional) :", bg="#F0F0F0",font=("calibri",11))

#next button
Screen1_next2 = tk.Button(root2,text="Next",font=("Calibri", 15))


button2.place(x=380,y=163)
button3.place(x=380,y=223)
label_2.place(x=100,y=167)
label_3.place(x=100,y=227)
Screen1_next2.place(x=600,y=325)



gui_MulT.place(x=320,y=4)
gui_descriptio_MulT.place(x=210,y=40)




#-------------------------------HebrewU 2 window------------------------------------------
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
Screen3_Optimize = tk.Button(root3,text="Optimize",font=("Calibri", 15))


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



root.mainloop()









