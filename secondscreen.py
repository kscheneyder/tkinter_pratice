from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from datetime import time
import numpy as np
import sqlalchemy
import pandas as pd


def connection():
    try:
        engine = sqlalchemy.create_engine(
            f'mysql+mysqlconnector://root:12345@localhost:3306/lardosidosos'
        )
        conn = engine.connect()
        print('DB conectado!')
        return conn
    except Exception as e:
        print(f'Erro ao tentar conectar com BD: {e}')


def read():
    query = """SELECT p.nome, m.descricao, h.Qtde, h.horario
                FROM horarios as h
                INNER JOIN medicamentos as m ON h.id_medicamento = m.id_medicamentos
                INNER JOIN pacientes as p ON h.Pacientes_cpf = p.cpf;"""
    with connection() as conn:
        df = pd.read_sql(sql=query, con = conn.connection)
    conn.commit()
    conn.close()
    return df


def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for row in read().itertuples(index=False):
        my_tree.insert(parent='', index='end', text='', values=(row.nome, row.descricao, row.horario, row.Qtde), tag='orow')
    my_tree.tag_configure('orow', background='#EEEEEE')


def setph(word,num):
    for ph in range(0,5):
        if ph == num:
            placeholderArray[ph].set(word)

def save():
    cpf = str(cpfEntry.get())
    id = str(idEntry.get())
    horario = str(horarioEntry.get())
    qtde = int(qtdeEntry.get())
    valid = True
    if not(cpf) or not(id) or not (horario) or not(qtde):
        messagebox.showwarning("", "Por favor preencha todas as entradas!")
        return 
    if len(cpf) < 11:
        messagebox.showwarning("","CPF invalido")
        return
    if not cpf.isdigit():
        messagebox.showwarning("","Digite o CPF apenas com números.")
        return
    try:
        query = f"""INSERT INTO horarios (Pacientes_cpf, id_medicamento, Horario, Qtde)
                    VALUES ('{cpf}','{id}','{horario}','{qtde}') """
        conn.execute(sqlalchemy.text(query))
        conn.commit()
        messagebox.showwarning("","Horario inserido com sucesso!")
    except Exception as e:
        messagebox.showerror("",f"Erro tentando salvar: {e}")
        return
    refreshTable()

def delete():
    try:
        if(my_tree.selection()[0]):
            decision = messagebox.askquestion("","Deletar o paciente selecionado?")
            if decision != 'yes':
                return
            else:
                selectedCPF = my_tree.selection()[0]
                CPFid = str(my_tree.item(selectedCPF)['values'][0])
                try:
                    query = f"DELETE FROM pacientes WHERE cpf = {CPFid}"
                    conn.execute(sqlalchemy.text(query))
                    conn.commit()
                    messagebox.showinfo("","Paciente deletado com sucesso.")
                except Exception as e:
                    messagebox.showinfo("",f"Erro ao deletar paciente. {e}")
                refreshTable()
    except:
        messagebox.showwarning("","Por favor selecione um paciente.")

def export_csv():
    query = """SELECT id_medicamento, Pacientes_cpf, Horario, Qtde
            FROM horarios
            ORDER BY 'Horario' ASC"""
    with connection() as conn:
        df = pd.read_sql(sql=query, con = conn.connection)
    conn.commit()
    messagebox.showinfo("","Arquivo exportado com sucesso.")
    return df.to_csv('LISTA_DE_HORARIOS.csv')


# frame=tk.Frame(window,bg="#02577A")
# frame.pack()
# manageFrame = tk.LabelFrame(frame,text="Manage",borderwidth=5)
# manageFrame.grid(row=0,column=0,sticky="w",padx=[10,200],pady=20,ipadx=[6])

window = tk.Tk()
window.title('Cadastro de Horarios')
window.geometry('720x520')
my_tree=ttk.Treeview(window,show='headings',height=20)
style = ttk.Style()


placeholderArray=['','','','','']
numeric='1234567890'
alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for i in range(0,5):
    placeholderArray[i]=tk.StringVar()

conn = connection()


saveBtn = Button(window, text="SALVAR", width=10,borderwidth=3,command=save).grid(row=5,column=1,sticky=tk.W,pady=4)
sairBtn = Button(window, text="SAIR", width=10,borderwidth=3,command=window.quit).grid(row=5,column=0,sticky=tk.W,pady=4)
deleteBtn = Button(window, text="DELETE", width=10,borderwidth=3,command=delete).grid(row=5,column=2,sticky=tk.W,pady=4)
exportBtn = Button(window, text="EXPORT CSV",width=10,borderwidth=3,command=export_csv).grid(row=5,column=3,sticky=tk.W,pady=4)
#window2Btn = Button(window, text="HORARIOS",width=15,borderwidth=3,command=open_window2).grid(row=6,column=0,sticky=tk.W,pady=4)

tk.Label(window, text="CPF Paciente").grid(row=1)
tk.Label(window, text="ID Medicamento").grid(row=2)
tk.Label(window, text="Horario").grid(row=3)
tk.Label(window, text="Qtde em ML").grid(row=4)

cpfEntry = tk.Entry(window)
idEntry = tk.Entry(window)
horarioEntry = tk.Entry(window)
qtdeEntry = tk.Entry(window)


cpfEntry.grid(row=1, column=1)
idEntry.grid(row=2, column=1)
horarioEntry.grid(row=3,column=1)
qtdeEntry.grid(row=4, column=1)



style.configure(window)
my_tree['columns'] = ("cpf","id","horario","qtde")
my_tree.column("#0",width = 0,stretch=NO)
my_tree.column("cpf", anchor=W,width=150)
my_tree.column("id",anchor=W,width=100)
my_tree.column("horario",anchor=W,width=75)
my_tree.column("qtde",anchor=W,width=50)
my_tree.heading("cpf",text="CPF",anchor=W)
my_tree.heading("id",text="Medicamento",anchor=W)
my_tree.heading("horario", text="Horario",anchor=W)
my_tree.heading("qtde",text="Quantidade em ML",anchor=W)
my_tree.tag_configure('orow',background="#EEEEEE")
my_tree.grid(row=6,column=1)
refreshTable()


window.resizable(False,False)
window.mainloop()