import tkinter
import os

global root
global RadioValue_Q1
global RadioValue_Q2
global RadioValue_Q3
global ScaleValue_Q1
global ScaleValue_Q2
global ScaleValue_Q3
global NameQ1
global NameQ2
global NameQ3
global LabelWin

root = tkinter.Tk()
RadioValue_Q1 = tkinter.DoubleVar()
RadioValue_Q2 = tkinter.DoubleVar()
RadioValue_Q3 = tkinter.DoubleVar()
ScaleValue_Q1 = tkinter.DoubleVar()
ScaleValue_Q2 = tkinter.DoubleVar()
ScaleValue_Q3 = tkinter.DoubleVar()
NameQ1 = tkinter.StringVar()
NameQ2 = tkinter.StringVar()
NameQ3 = tkinter.StringVar()
LabelWin = tkinter.LabelFrame(root, text="Paramétrage des quêtes", padx=5, pady=5)


def InitTkinter():

    LabelQ1 = tkinter.LabelFrame(LabelWin, text="Quête 1", padx=5, pady=5)
    Frame_Q1_1 = tkinter.Frame(LabelQ1, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q1_2 = tkinter.Frame(LabelQ1, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q1_3 = tkinter.Frame(LabelQ1, width=0, height=50, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q1_4 = tkinter.Frame(LabelQ1, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Quest1Name = tkinter.Entry(Frame_Q1_1, textvariable=NameQ1, width=60)
    listeQ1 = tkinter.Listbox(Frame_Q1_3, height=13)
    listeQ1.insert(tkinter.END, "Archer")
    listeQ1.insert(tkinter.END, "Catapulte 1")
    listeQ1.insert(tkinter.END, "Catapulte 2")
    listeQ1.insert(tkinter.END, "Catapulte 3")
    listeQ1.insert(tkinter.END, "Catapulte 4")
    listeQ1.insert(tkinter.END, "Baliste")
    listeQ1.insert(tkinter.END, "Loup")
    listeQ1.insert(tkinter.END, "Gobelin")
    listeQ1.insert(tkinter.END, "Golem")
    listeQ1.insert(tkinter.END, "Orc")
    listeQ1.insert(tkinter.END, "Chevalier")
    listeQ1.insert(tkinter.END, "Nain")
    listeQ1.insert(tkinter.END, "Dragon")
    listeQ1.insert(tkinter.END, "Fantome")
    SpinBoxQ1 = tkinter.Spinbox(Frame_Q1_4, from_=0, to=1000)

    LabelQ2 = tkinter.LabelFrame(LabelWin, text="Quête 2", padx=5, pady=5)
    Frame_Q2_1 = tkinter.Frame(LabelQ2, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q2_2 = tkinter.Frame(LabelQ2, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q2_3 = tkinter.Frame(LabelQ2, width=0, height=50, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q2_4 = tkinter.Frame(LabelQ2, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Quest2Name = tkinter.Entry(Frame_Q2_1, textvariable=NameQ2, width=60)
    listeQ2 = tkinter.Listbox(Frame_Q2_3, height=13)
    listeQ2.insert(tkinter.END, "Archer")
    listeQ2.insert(tkinter.END, "Catapulte 1")
    listeQ2.insert(tkinter.END, "Catapulte 2")
    listeQ2.insert(tkinter.END, "Catapulte 3")
    listeQ2.insert(tkinter.END, "Catapulte 4")
    listeQ2.insert(tkinter.END, "Baliste")
    listeQ2.insert(tkinter.END, "Loup")
    listeQ2.insert(tkinter.END, "Gobelin")
    listeQ2.insert(tkinter.END, "Golem")
    listeQ2.insert(tkinter.END, "Orc")
    listeQ2.insert(tkinter.END, "Chevalier")
    listeQ2.insert(tkinter.END, "Nain")
    listeQ2.insert(tkinter.END, "Dragon")
    SpinBoxQ2 = tkinter.Spinbox(Frame_Q2_4, from_=0, to=1000)

    LabelQ3 = tkinter.LabelFrame(LabelWin, text="Quête 3", padx=5, pady=5)
    Frame_Q3_1 = tkinter.Frame(LabelQ3, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q3_2 = tkinter.Frame(LabelQ3, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q3_3 = tkinter.Frame(LabelQ3, width=0, height=50, borderwidth=2, relief=tkinter.GROOVE)
    Frame_Q3_4 = tkinter.Frame(LabelQ3, width=0, height=0, borderwidth=2, relief=tkinter.GROOVE)
    Quest3Name = tkinter.Entry(Frame_Q3_1, textvariable=NameQ3, width=60)
    listeQ3 = tkinter.Listbox(Frame_Q3_3, height=13)
    listeQ3.insert(tkinter.END, "Archer")
    listeQ3.insert(tkinter.END, "Catapulte 1")
    listeQ3.insert(tkinter.END, "Catapulte 2")
    listeQ3.insert(tkinter.END, "Catapulte 3")
    listeQ3.insert(tkinter.END, "Catapulte 4")
    listeQ3.insert(tkinter.END, "Baliste")
    listeQ3.insert(tkinter.END, "Loup")
    listeQ3.insert(tkinter.END, "Gobelin")
    listeQ3.insert(tkinter.END, "Golem")
    listeQ3.insert(tkinter.END, "Orc")
    listeQ3.insert(tkinter.END, "Chevalier")
    listeQ3.insert(tkinter.END, "Nain")
    listeQ3.insert(tkinter.END, "Dragon")
    SpinBoxQ3 = tkinter.Spinbox(Frame_Q3_4, from_=0, to=1000)


def SaveQuests(filename):
    dirname, filename = os.path.split(filename)
    filename, ext = os.path.splitext(filename)
    with open(dirname + "/QuestFiles/" + filename + ".json", "w") as f:
        f.write("{\n")
        f.write('    FirstQuestName  : "' + NameQ1.get() + '",\n')
        f.write('    SecondQuestName : "' + NameQ2.get() + '",\n')
        f.write('    ThirdQuestName  : "' + NameQ3.get() + '",\n')
        f.write("\n")
        f.write("    FirstQuestObjectif  : " + str(RadioValue_Q1.get()) + ",\n")
        f.write("    SecondQuestObjectif : " + str(RadioValue_Q2.get()) + ",\n")
        f.write("    ThirdQuestObjectif  : " + str(RadioValue_Q3.get()) + ",\n")
        f.write("}")


def ModifQuests():

    LabelWin.pack(fill="both", expand="yes")

    LabelQ1.pack(side=tkinter.LEFT, fill="both", expand="yes")
    Frame_Q1_1.pack(side=tkinter.TOP, padx=5, pady=5)
    Frame_Q1_2.pack(side=tkinter.LEFT, padx=5, pady=5)
    Frame_Q1_3.pack(side=tkinter.BOTTOM, padx=5, pady=5)
    Frame_Q1_4.pack(side=tkinter.BOTTOM, padx=5, pady=5)
    tkinter.Label(Frame_Q1_1, text="Quest name :").pack(side=tkinter.TOP)
    Quest1Name.pack()
    tkinter.Radiobutton(Frame_Q1_2, text="            Acheter une tour", variable=RadioValue_Q1, value=1).pack()
    tkinter.Radiobutton(Frame_Q1_2, text="Tuer un certain nb d'ennemis", variable=RadioValue_Q1, value=2).pack()
    tkinter.Radiobutton(Frame_Q1_2, text="    Atteindre un niveau d'or", variable=RadioValue_Q1, value=3).pack()
    listeQ1.pack()
    SpinBoxQ1.pack(side=tkinter.RIGHT)

    LabelQ2.pack(side=tkinter.LEFT, fill="both", expand="yes")
    Frame_Q2_1.pack(side=tkinter.TOP, padx=5, pady=5)
    Frame_Q2_2.pack(side=tkinter.LEFT, padx=5, pady=5)
    Frame_Q2_3.pack(side=tkinter.BOTTOM, padx=5, pady=5)
    Frame_Q2_4.pack(side=tkinter.BOTTOM, padx=5, pady=5)
    tkinter.Label(Frame_Q2_1, text="Quest name :").pack(side=tkinter.TOP)
    Quest2Name.pack()
    tkinter.Radiobutton(Frame_Q2_2, text="            Acheter une tour", variable=RadioValue_Q2, value=1).pack()
    tkinter.Radiobutton(Frame_Q2_2, text="Tuer un certain nb d'ennemis", variable=RadioValue_Q2, value=2).pack()
    tkinter.Radiobutton(Frame_Q2_2, text="    Atteindre un niveau d'or", variable=RadioValue_Q2, value=3).pack()
    listeQ2.pack()
    SpinBoxQ2.pack(side=tkinter.RIGHT)

    LabelQ3.pack(side=tkinter.LEFT, fill="both", expand="yes")
    Frame_Q3_1.pack(side=tkinter.TOP, padx=5, pady=5)
    Frame_Q3_2.pack(side=tkinter.LEFT, padx=5, pady=5)
    Frame_Q3_3.pack(side=tkinter.BOTTOM, padx=5, pady=5)
    Frame_Q3_4.pack(side=tkinter.BOTTOM, padx=5, pady=5)
    tkinter.Label(Frame_Q3_1, text="Quest name :").pack(side=tkinter.TOP)
    Quest3Name.pack()
    tkinter.Radiobutton(Frame_Q3_2, text="            Acheter une tour", variable=RadioValue_Q3, value=1).pack()
    tkinter.Radiobutton(Frame_Q3_2, text="Tuer un certain nb d'ennemis", variable=RadioValue_Q3, value=2).pack()
    tkinter.Radiobutton(Frame_Q3_2, text="    Atteindre un niveau d'or", variable=RadioValue_Q3, value=3).pack()
    listeQ3.pack()
    SpinBoxQ3.pack(side=tkinter.RIGHT)

    root.mainloop()
