from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
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
    query = """SELECT  cpf, Nome, DataNascimento, Idade
            FROM pacientes
            ORDER BY 'Nome' ASC"""
    with connection() as conn:
        df = pd.read_sql(sql=query, con = conn.connection)
    conn.commit()
    conn.close()
    return df


def refreshTable():
    try:
        query_datareferencia = """UPDATE pacientes SET DataReferencia = CURDATE();"""
        conn.execute(sqlalchemy.text(query_datareferencia))
        conn.commit()
        print('Data Referencia Atualizada')
    except Exception as e:
        print(f'Data não atualizada, erro: {e}')

    try:
        query_datareferencia = """UPDATE pacientes
                                SET Idade = TIMESTAMPDIFF(YEAR, DataNascimento, DataReferencia);"""
        conn.execute(sqlalchemy.text(query_datareferencia))
        conn.commit()
        print('Idade atualizada')
    except Exception as e:
        print(f'Idade não atualizada, erro: {e}')
    for data in my_tree.get_children():
        my_tree.delete(data)
    for row in read().itertuples(index=False):
        my_tree.insert(parent='', index='end', iid=row.cpf, text='', values=(row.cpf, row.Nome, row.DataNascimento, row.Idade), tag='orow')
    my_tree.tag_configure('orow', background='#EEEEEE')


def setph(word,num):
    for ph in range(0,5):
        if ph == num:
            placeholderArray[ph].set(word)

def save():
    cpf = str(cpfEntry.get())
    nome = str(nomeEntry.get())
    data = str(dataEntry.get())
    valid = True
    if not(cpf) or not(nome) or not (data):
        messagebox.showwarning("", "Por favor preencha todas as entradas!")
        return 
    if len(cpf) < 11:
        messagebox.showwarning("","CPF invalido")
        return
    if not cpf.isdigit():
        messagebox.showwarning("","Digite o CPF apenas com números.")
        return
    try:
        query = f"""SELECT * FROM pacientes WHERE cpf = '{cpf}' """
        df = pd.read_sql(sql = query, con = conn.connection)
        if len(df) > 0:
            messagebox.showwarning("","CPF já esta em uso.")
            return
        else:
            query = f"""INSERT INTO pacientes (cpf, Nome, DataNascimento)
                        VALUES ('{cpf}','{nome}','{data}') """
            conn.execute(sqlalchemy.text(query))
            conn.commit()
            messagebox.showwarning("","Paciente inserido com sucesso!")
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
    query = """SELECT  cpf, Nome, DataNascimento, Idade
            FROM pacientes
            ORDER BY 'Nome' ASC"""
    with connection() as conn:
        df = pd.read_sql(sql=query, con = conn.connection)
    conn.commit()
    messagebox.showinfo("","Arquivo exportado com sucesso.")
    return df.to_csv('LISTA_DE_PACIENTES.csv')


# frame=tk.Frame(window,bg="#02577A")
# frame.pack()
# manageFrame = tk.LabelFrame(frame,text="Manage",borderwidth=5)
# manageFrame.grid(row=0,column=0,sticky="w",padx=[10,200],pady=20,ipadx=[6])

window = tk.Tk()
window.title('Cadastro de Pacientes')
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
tk.Label(window, text="Nome").grid(row=2)
tk.Label(window, text="Data de Nascimento").grid(row=3)

cpfEntry = tk.Entry(window)
nomeEntry = tk.Entry(window)
dataEntry = tk.Entry(window)

cpfEntry.grid(row=1, column=1)
nomeEntry.grid(row=2, column=1)
dataEntry.grid(row=3, column=1)


style.configure(window)
my_tree['columns'] = ("cpf","nome","DataNascimento","Idade")
my_tree.column("#0",width = 0,stretch=NO)
my_tree.column("cpf", anchor=W,width=100)
my_tree.column("nome",anchor=W,width=125)
my_tree.column("DataNascimento",anchor=W,width=125)
my_tree.column("Idade",anchor=W,width=70)
my_tree.heading("cpf",text="CPF",anchor=W)
my_tree.heading("nome",text="Nome",anchor=W)
my_tree.heading("DataNascimento", text="Data de Nascimento",anchor=W)
my_tree.heading("Idade",text="Idade",anchor=W)
my_tree.tag_configure('orow',background="#EEEEEE")
my_tree.grid(row=6,column=1)
refreshTable()


window.resizable(False,False)
window.mainloop()