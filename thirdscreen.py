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
    query = """SELECT id_medicamentos, descricao
            FROM medicamentos
            ORDER BY 'id_medicamentos' ASC"""
    with connection() as conn:
        df = pd.read_sql(sql=query, con = conn.connection)
    conn.commit()
    conn.close()
    return df


def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for row in read().itertuples(index=False):
        my_tree.insert(parent='', index='end', text='', values=(row.id_medicamentos, row.descricao), tag='orow')
    my_tree.tag_configure('orow', background='#EEEEEE')


def setph(word,num):
    for ph in range(0,5):
        if ph == num:
            placeholderArray[ph].set(word)

def save():
    id = str(idEntry.get())
    descricao = str(descricaoEntry.get())
    valid = True
    if not(id) or not(descricao):
        messagebox.showwarning("", "Por favor preencha todas as entradas!")
        return 
    if not id.isdigit():
        messagebox.showwarning("","Digite o ID do medicamento apenas com números.")
        return
    try:
        query = f"""INSERT INTO medicamentos (id_medicamentos, descricao)
                    VALUES ('{id}','{descricao}') """
        conn.execute(sqlalchemy.text(query))
        conn.commit()
        messagebox.showwarning("","Medicamento inserido com sucesso!")
    except Exception as e:
        messagebox.showerror("",f"Erro tentando salvar: {e}")
        return
    refreshTable()

def delete():
    try:
        if(my_tree.selection()[0]):
            decision = messagebox.askquestion("","Deletar o medicamento selecionado?")
            if decision != 'yes':
                return
            else:
                selectedID = my_tree.selection()[0]
                id = str(my_tree.item(selectedID)['values'][0])
                try:
                    query = f"DELETE FROM medicamentos WHERE id_medicamentos = {id}"
                    conn.execute(sqlalchemy.text(query))
                    conn.commit()
                    messagebox.showinfo("","Medicamento deletado com sucesso.")
                except Exception as e:
                    messagebox.showinfo("",f"Erro ao deletar medicamento. {e}")
                refreshTable()
    except:
        messagebox.showwarning("","Por favor selecione um medicamento.")

def export_csv():
    query = """SELECT id_medicamentos, descricao
            FROM medicamentos
            ORDER BY 'id_medicamentos' ASC"""
    with connection() as conn:
        df = pd.read_sql(sql=query, con = conn.connection)
    conn.commit()
    messagebox.showinfo("","Arquivo exportado com sucesso.")
    return df.to_csv('LISTA_DE_MEDICAMENTOS.csv')


# frame=tk.Frame(window,bg="#02577A")
# frame.pack()
# manageFrame = tk.LabelFrame(frame,text="Manage",borderwidth=5)
# manageFrame.grid(row=0,column=0,sticky="w",padx=[10,200],pady=20,ipadx=[6])

window = tk.Tk()
window.title('Cadastro de Medicamentos')
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

tk.Label(window, text="ID Medicamento").grid(row=1)
tk.Label(window, text="Descricao").grid(row=2)

idEntry = tk.Entry(window)
descricaoEntry = tk.Entry(window)


idEntry.grid(row=1, column=1)
descricaoEntry.grid(row=2, column=1)


style.configure(window)
my_tree['columns'] = ("id","descricao")
my_tree.column("#0",width = 0,stretch=NO)
my_tree.column("id", anchor=W,width=100)
my_tree.column("descricao",anchor=W,width=150)
my_tree.heading("id",text="ID Medicamento",anchor=W)
my_tree.heading("descricao",text="Descrição",anchor=W)
my_tree.tag_configure('orow',background="#EEEEEE")
my_tree.grid(row=6,column=1)
refreshTable()


window.resizable(False,False)
window.mainloop()