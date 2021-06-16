import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msb
from tkinter import *
import sqlite3

root = Tk()
root.title("Boletim Escolar")
width = 1000
height = 400
sc_width = root.winfo_screenwidth()
sc_height = root.winfo_screenheight()
x = (sc_width/2) - (width/2)
y = (sc_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.iconbitmap("boletim.ico")
root.config(bg="deep sky blue")

disciplina = StringVar()
av1 = DoubleVar()
av2 = DoubleVar()
avd = DoubleVar()
media = DoubleVar()
avs = DoubleVar()
avds = DoubleVar()
mediaFinal = DoubleVar()
resultadoFinal = StringVar()
aprovado = 'Aprovado'
reprovado = 'Reprovado'
updateWindow = None
id = None
newWindow = None

def database():
    conn = sqlite3.connect("boletim.db")
    cursor = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS 'materia' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                disciplina TEXT, av1 DOUBLE, av2 DOUBLE, avd DOUBLE, media DOUBLE, avs DOUBLE, avds DOUBLE, mediaFinal DOUBLE, resultadoFinal TEXT) """
    cursor.execute(query)
    cursor.execute('SELECT * FROM materia ORDER BY disciplina')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def submitData():
    try:
        if disciplina.get() == "" or av1.get() < 0 or av1.get() > 10 or av2.get() < 0 or av2.get() > 10 or avd.get() < 0 or avd.get() > 10 or avs.get() < 0 or avs.get() > 10 or avd.get() > 10 or avds.get() < 0 or avds.get() > 10:
            resultado = msb.showwarning(
                "Campo Inválido", "Por favor, digite todos os campos com valores válidos (Notas de 0 a 10). Caso não tenha feito alguma avaliação, preencha o campo com 0", icon="warning")
        else:
            m = (av1.get()+av2.get()+avd.get())/3
            media.set(m)
            if av1.get() >= avs.get() and av2.get() >= avs.get() and avd.get() >= avds.get():
                mediaFinal.set(media.get())
            else:
                if av1.get() >= avs.get() and av2.get() >= avs.get() and avd.get() < avds.get():
                    mediaFinal.set((av1.get()+av2.get()+avds.get())/3)
                else:
                    if av1.get() <= av2.get() and av1.get() <= avs.get() and avd.get() >= avds.get():
                        mediaFinal.set((avs.get()+av2.get()+avd.get())/3)
                    else:
                        if av1.get() <= av2.get() and av1.get() <= avs.get() and avd.get() < avds.get():
                            mediaFinal.set((avs.get()+av2.get()+avds.get())/3)
                        else:
                            if av1.get() >= av2.get() and avs.get() >= av2.get() and avd.get() >= avds.get():
                                mediaFinal.set((av1.get()+avs.get()+avd.get())/3)
                            else:
                                if av1.get() >= av2.get() and avs.get() >= av2.get() and avd.get() < avds.get():
                                    mediaFinal.set((av1.get()+avs.get()+avds.get())/3)
            if av1.get() >= 4 and av2.get() >= 4 and avd.get() >= 4:
                if mediaFinal.get() >= 6.0:
                    resultadoFinal.set(aprovado)
                else:
                    resultadoFinal.set(reprovado)
            else:
                if av1.get() < 4 and av2.get() >= 4 and avd.get() >= 4 and avs.get() >= 4:
                    if mediaFinal.get() >= 6.0:
                        resultadoFinal.set(aprovado)
                    else:
                        resultadoFinal.set(reprovado)
                else:
                    if av1.get() >= 4 and av2.get() < 4 and avd.get() >= 4 and avs.get() >= 4:
                        if mediaFinal.get() >= 6.0:
                            resultadoFinal.set(aprovado)
                        else:
                            resultadoFinal.set(reprovado)
                    else:
                        if av1.get() >= 4 and av2.get() >= 4 and avd.get() < 4 and avds.get() >= 4:
                            if mediaFinal.get() >= 6.0:
                                resultadoFinal.set(aprovado)
                            else:
                                resultadoFinal.set(reprovado)
                        else:
                            if av1.get() < 4 and av2.get() >= 4 and avd.get() < 4 and avds.get() >= 4 and avs.get() >= 4:
                                if mediaFinal.get() >= 6.0:
                                    resultadoFinal.set(aprovado)
                                else:
                                    resultadoFinal.set(reprovado)
                            else:
                                if av1.get() >= 4 and av2.get() < 4 and avd.get() < 4 and avs.get() >= 4 and avds.get() >= 4:
                                    if mediaFinal.get() >= 6:
                                        resultadoFinal.set(aprovado)
                                    else:
                                        resultadoFinal.set(reprovado)
                                else:
                                    resultadoFinal.set(reprovado)


            tree.delete(*tree.get_children())
            conn = sqlite3.connect("boletim.db")
            cursor = conn.cursor()
            query = """ INSERT INTO 'materia' (disciplina,av1,av2,avd,media,avs,avds,mediaFinal,resultadoFinal) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query,
                        (str(disciplina.get()),
                            float(format(av1.get(), '.2f')),
                            float(format(av2.get(), '.2f')),
                            float(format(avd.get(), '.2f')),
                            float(format(media.get(), '.2f')),
                            float(format(avs.get(), '.2f')),
                            float(format(avds.get(), '.2f')),
                            float(format(mediaFinal.get(), '.2f')),
                            str(resultadoFinal.get())))
            conn.commit()
            cursor.execute('SELECT * FROM materia ORDER BY disciplina')
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()
            disciplina.set("")
            resultadoFinal.set("")
    except TclError:
        resultado2 = msb.showwarning(
            "Campo Inválido", "Por favor, digite apenas NÚMEROS nos campos destinado a notas. Utilize pontos( . ) em vez de virgulas ( , ) para indicar números decimais e não deixe zeros a esquerda", icon="warning")

def updateData():
    try:
        if disciplina.get() == "" or av1.get() < 0 or av1.get() > 10 or av2.get() < 0 or av2.get() > 10 or avd.get() < 0 or avd.get() > 10 or avs.get() < 0 or avs.get() > 10 or avd.get() > 10 or avds.get() < 0 or avds.get() > 10:
            resultado3 = msb.showwarning(
                "Campo Inválido", "Por favor, digite todos os campos com valores válidos (Notas de 0 a 10). Caso não tenha feito alguma avaliação, preencha o campo com 0", icon="warning")
        else:
            
            
            m = (av1.get()+av2.get()+avd.get())/3
            media.set(m)
            if av1.get() >= avs.get() and av2.get() >= avs.get() and avd.get() >= avds.get():
                mediaFinal.set(media.get())
            else:
                if av1.get() >= avs.get() and av2.get() >= avs.get() and avd.get() < avds.get():
                    mediaFinal.set((av1.get()+av2.get()+avds.get())/3)
                else:
                    if av1.get() <= av2.get() and av1.get() <= avs.get() and avd.get() >= avds.get():
                        mediaFinal.set((avs.get()+av2.get()+avd.get())/3)
                    else:
                        if av1.get() <= av2.get() and av1.get() <= avs.get() and avd.get() < avds.get():
                            mediaFinal.set((avs.get()+av2.get()+avds.get())/3)
                        else:
                            if av1.get() >= av2.get() and avs.get() >= av2.get() and avd.get() >= avds.get():
                                mediaFinal.set((av1.get()+avs.get()+avd.get())/3)
                            else:
                                if av1.get() >= av2.get() and avs.get() >= av2.get() and avd.get() < avds.get():
                                    mediaFinal.set((av1.get()+avs.get()+avds.get())/3)
            if av1.get() >= 4 and av2.get() >= 4 and avd.get() >= 4:
                if mediaFinal.get() >= 6.0:
                    resultadoFinal.set(aprovado)
                else:
                    resultadoFinal.set(reprovado)
            else:
                if av1.get() < 4 and av2.get() >= 4 and avd.get() >= 4 and avs.get() >= 4:
                    if mediaFinal.get() >= 6.0:
                        resultadoFinal.set(aprovado)
                    else:
                        resultadoFinal.set(reprovado)
                else:
                    if av1.get() >= 4 and av2.get() < 4 and avd.get() >= 4 and avs.get() >= 4:
                        if mediaFinal.get() >= 6.0:
                            resultadoFinal.set(aprovado)
                        else:
                            resultadoFinal.set(reprovado)
                    else:
                        if av1.get() >= 4 and av2.get() >= 4 and avd.get() < 4 and avds.get() >= 4:
                            if mediaFinal.get() >= 6.0:
                                resultadoFinal.set(aprovado)
                            else:
                                resultadoFinal.set(reprovado)
                        else:
                            if av1.get() < 4 and av2.get() >= 4 and avd.get() < 4 and avds.get() >= 4 and avs.get() >= 4:
                                if mediaFinal.get() >= 6.0:
                                    resultadoFinal.set(aprovado)
                                else:
                                    resultadoFinal.set(reprovado)
                            else:
                                if av1.get() >= 4 and av2.get() < 4 and avd.get() < 4 and avs.get() >= 4 and avds.get() >= 4:
                                    if mediaFinal.get() >= 6:
                                        resultadoFinal.set(aprovado)
                                    else:
                                        resultadoFinal.set(reprovado)
                                else:
                                    resultadoFinal.set(reprovado)


            tree.delete(*tree.get_children())
            conn = sqlite3.connect("boletim.db")
            cursor = conn.cursor()
            query = """ UPDATE 'materia' SET disciplina = ?, av1 = ?, av2 = ?, avd = ?, media = ?, avs = ?, avds = ?, mediaFinal = ?, resultadoFinal = ? WHERE id = ?"""
            cursor.execute(query,
                        (str(disciplina.get()),
                            float(format(av1.get(), '.2f')),
                            float(format(av2.get(), '.2f')),
                            float(format(avd.get(), '.2f')),
                            float(format(media.get(), '.2f')),
                            float(format(avs.get(), '.2f')),
                            float(format(avds.get(), '.2f')),
                            float(format(mediaFinal.get(), '.2f')),
                            str(resultadoFinal.get()),
                            int(id)))
            conn.commit()
            cursor.execute('SELECT * FROM materia ORDER BY disciplina')
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()
            disciplina.set("")
            av1.set(0)
            av2.set(0)
            avd.set(0)
            avs.set(0)
            avds.set(0)
            media.set(0)
            mediaFinal.set(0)
            resultadoFinal.set("")
            updateWindow.destroy()
    except TclError:
        resultado4 = msb.showwarning(
            "Campo Inválido", "Por favor, digite apenas NÚMEROS nos campos destinado a notas. Utilize pontos( . ) em vez de virgulas ( , ) para indicar números decimais e não deixe zeros a esquerda", icon="warning")

def onSelect(event):
    global id, updateWindow
    selectItem = tree.focus()
    conteudo = (tree.item(selectItem))
    selectedItem = conteudo["values"]
    id = selectedItem[0]
    disciplina.set("")
    av1.set(0)
    av2.set(0)
    avd.set(0)
    avs.set(0)
    avds.set(0)
    media.set(0)
    mediaFinal.set(0)
    resultadoFinal.set("")
    disciplina.set(selectedItem[1])
    av1.set(selectedItem[2])
    av2.set(selectedItem[3])
    avd.set(selectedItem[4])
    media.set(selectedItem[5])
    avs.set(selectedItem[6])
    avds.set(selectedItem[7])
    mediaFinal.set(selectedItem[8])
    resultadoFinal.set(selectedItem[9])

    updateWindow = Toplevel()
    updateWindow.title("ATUALIZAR NOTAS")
    width = 480
    heigth = 200
    sc_width = updateWindow.winfo_screenwidth()
    sc_height = updateWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    updateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateWindow.resizable(0, 0)

    formTitle = Frame(updateWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(updateWindow)
    formContact.pack(side=TOP, pady=10)
   
    lbl_title = Label(formTitle, text="Atualizando Disciplina",
                      font=('arial', 18), bg='blue', width=300)
    lbl_title.pack(fill=X)

    lbl_disciplina = Label(formContact, text="Disciplina", font=('arial', 12))
    lbl_disciplina.grid(row=0, sticky=W)

    lbl_av1 = Label(formContact, text="Av1", font=('arial', 12))
    lbl_av1.grid(row=1, sticky=W)

    lbl_av2 = Label(formContact, text="Av2", font=('arial', 12))
    lbl_av2.grid(row=2, sticky=W)

    lbl_avd = Label(formContact, text="AvD", font=('arial', 12))
    lbl_avd.grid(row=3, sticky=W)

    lbl_avs = Label(formContact, text="AvS", font=('arial', 12))
    lbl_avs.grid(row=4, sticky=W)

    lbl_avds = Label(formContact, text="AvDS", font=('arial', 12))
    lbl_avds.grid(row=5, sticky=W)

    disciplinaEntry = Entry(
        formContact, textvariable=disciplina, font=('arial', 12))
    disciplinaEntry.grid(row=0, column=1)

    av1Entry = Entry(formContact, textvariable=av1, font=('arial', 12))
    av1Entry.grid(row=1, column=1)

    av2Entry = Entry(formContact, textvariable=av2, font=('arial', 12))
    av2Entry.grid(row=2, column=1)

    avdEntry = Entry(formContact, textvariable=avd, font=('arial', 12))
    avdEntry.grid(row=3, column=1)

    avsEntry = Entry(formContact, textvariable=avs, font=('arial', 12))
    avsEntry.grid(row=4, column=1)

    avdsEntry = Entry(formContact, textvariable=avds, font=('arial', 12))
    avdsEntry.grid(row=5, column=1)

    bttn_update = Button(formContact, text="Atualizar",
                         width=50, command=updateData)
    bttn_update.grid(row=6, columnspan=2, pady=10)


def deletarData():
    if not tree.selection():
        resultado = msb.showwarning(
            "Item não selecionado", "Por favor, selecione um item na lista.", icon="warning")
    else:
        resultado = msb.askquestion(
            "Excluir Disciplina Selecionada", "Tem certeza que deseja deletar a Disciplina?")
        if resultado == 'yes':
            selectItem = tree.focus()
            conteudo = (tree.item(selectItem))
            selectedItem = conteudo['values']
            tree.delete(selectItem)
            conn = sqlite3.connect("boletim.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM 'materia' WHERE id = %d" %
                           selectedItem[0])
            conn.commit()
            cursor.close()
            conn.close()


def inserirData():
    global newWindow
    disciplina.set("")
    resultadoFinal.set("")

    newWindow = Toplevel()
    newWindow.title("INSERINDO DISCIPLINA")
    width = 480
    heigth = 200
    sc_width = newWindow.winfo_screenwidth()
    sc_height = newWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    newWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newWindow.resizable(0, 0)

    formTitle = Frame(newWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(newWindow)
    formContact.pack(side=TOP, pady=10)
   
    lbl_title = Label(formTitle, text="Inserindo disciplina",
                      font=('arial', 18), bg='blue', width=300)
    lbl_title.pack(fill=X)

    lbl_disciplina = Label(formContact, text="Disciplina", font=('arial', 12))
    lbl_disciplina.grid(row=0, sticky=W)

    lbl_av1 = Label(formContact, text="Av1", font=('arial', 12))
    lbl_av1.grid(row=1, sticky=W)

    lbl_av2 = Label(formContact, text="Av2", font=('arial', 12))
    lbl_av2.grid(row=2, sticky=W)

    lbl_avd = Label(formContact, text="AvD", font=('arial', 12))
    lbl_avd.grid(row=3, sticky=W)

    lbl_avs = Label(formContact, text="AvS", font=('arial', 12))
    lbl_avs.grid(row=5, sticky=W)

    lbl_avds = Label(formContact, text="AvDS", font=('arial', 12))
    lbl_avds.grid(row=6, sticky=W)

    disciplinaEntry = Entry(
        formContact, textvariable=disciplina, font=('arial', 12))
    disciplinaEntry.grid(row=0, column=1)

    av1Entry = Entry(formContact, textvariable=av1, font=('arial', 12))
    av1Entry.grid(row=1, column=1)

    av2Entry = Entry(formContact, textvariable=av2, font=('arial', 12))
    av2Entry.grid(row=2, column=1)

    avdEntry = Entry(formContact, textvariable=avd, font=('arial', 12))
    avdEntry.grid(row=3, column=1)

    avsEntry = Entry(formContact, textvariable=avs, font=('arial', 12))
    avsEntry.grid(row=5, column=1)

    avdsEntry = Entry(formContact, textvariable=avds, font=('arial', 12))
    avdsEntry.grid(row=6, column=1)

    bttn_inserir = Button(formContact, text="Inserir",
                          width=50, command=submitData)
    bttn_inserir.grid(row=7, columnspan=2, pady=10)


def sobreApp():
    global newWindow
    newWindow = Toplevel()
    newWindow.title("INFORMAÇÕES DO APLICATIVO")
    width = 480
    heigth = 100
    sc_width = newWindow.winfo_screenwidth()
    sc_height = newWindow.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    newWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newWindow.resizable(0, 0)

    formTitle = Frame(newWindow)
    formTitle.pack(side=TOP)
    formContact = Frame(newWindow)
    formContact.pack(side=TOP, pady=10)
    lbl_title = Label(formTitle, text="INFORMAÇÕES DO DESENVOLVEDOR", font=(
        'arial', 18), bg='deep sky blue', width=300)
    lbl_title.pack(fill=X)

    lbl_informacao = Label(formContact,
                           text="Aplicatico desenvolvido por: \nGuilherme Leite de Sousa Lima \nMatricula: 202003392804", font=('arial', 12))
    lbl_informacao.grid(row=3, sticky=W)

top = Frame(root, width=500, bd=1, relief=SOLID)
top.pack(side=TOP)
mid = Frame(root, width=500, bg="deep sky blue")
mid.pack(side=TOP)
midLeft = Frame(mid, width=100)
midLeft.pack(side=LEFT)
midLeftPadding = Frame(mid, width=350, bg="deep sky blue")
midLeftPadding.pack(side=LEFT)
midRight = Frame(mid, width=100)
midRight.pack(side=RIGHT)
bottom = Frame(root, width=200)
bottom.pack(side=BOTTOM)
tableMargim = Frame(root, width=500)
tableMargim.pack(side=TOP)

lbl_title = Label(top, text="SISTEMA DE CONTROLE DE NOTAS (BOLETIM)",
                  bg="white", font=('arial', 18), width=500)
lbl_title.pack(fill=X)

lbl_alt = Label(bottom, text="Para alterar clique duas vezes na disciplina desejada.",
                bg="deep sky blue", font=('arial', 12), width=200)
lbl_alt.pack(fill=X)

bttn_add = Button(midLeft, text="Inserir",
                  bg="light blue", command=inserirData)
bttn_add.pack()
bttn_del = Button(midRight, text="Deletar",
                  bg="firebrick1", command=deletarData)
bttn_del.pack(side=RIGHT)

scrollbarX = Scrollbar(tableMargim, orient=HORIZONTAL)
scrollbarY = Scrollbar(tableMargim, orient=VERTICAL)

tree = ttk.Treeview(tableMargim, columns=("ID", "Disciplina", "Av1", "Av2", "AvD", "Media", "AvS", "AvDS", "Media Final", "Resultado Final"), height=400,
                    selectmode="extended", yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
scrollbarY.config(command=tree.yview)
scrollbarY.pack(side=RIGHT, fill=Y)
scrollbarX.config(command=tree.xview)
scrollbarX.pack(side=BOTTOM, fill=X)
tree.heading("ID", text="ID", anchor=W)
tree.heading("Disciplina", text="Disciplina", anchor=W)
tree.heading("Av1", text="Av1", anchor=W)
tree.heading("Av2", text="Av2", anchor=W)
tree.heading("AvD", text="AvD", anchor=W)
tree.heading("Media", text="Media", anchor=W)
tree.heading("AvS", text="AvS", anchor=W)
tree.heading("AvDS", text="AvDS", anchor=W)
tree.heading("Media Final", text="Media Final", anchor=W)
tree.heading("Resultado Final", text="Resultado Final", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=1)
tree.column('#1', stretch=NO, minwidth=0, width=20)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=80)
tree.column('#7', stretch=NO, minwidth=0, width=80)
tree.column('#8', stretch=NO, minwidth=0, width=80)
tree.column('#9', stretch=NO, minwidth=0, width=80)
tree.pack()
tree.bind('<Double-Button-1>', onSelect)

menu_bar = Menu(root)
root.config(menu=menu_bar)

fileMenu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=fileMenu)
fileMenu.add_command(label="Criar Novo", command=inserirData)
fileMenu.add_separator()
fileMenu.add_command(label="Sair", command=root.destroy)

menuSobre = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Sobre", menu=menuSobre)
menuSobre.add_command(label="Info", command=sobreApp)

if __name__ == '__main__':
    database()
    root.mainloop()
