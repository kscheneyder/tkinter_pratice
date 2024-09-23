import tkinter as tk
import subprocess

def abrir_programa1():
    subprocess.Popen(['python','firstscreen.py'])

def abrir_programa2():
    subprocess.Popen(['python','secondscreen.py'])

def abrir_programa3():
    subprocess.Popen(['python','thirdscreen.py'])

janela = tk.Tk()
janela.title("Menu Principal")

janela.geometry("300x200")


# Botões para abrir os programas
botao1 = tk.Button(janela, text="Cadastro de Pacientes", command=abrir_programa1)
botao1.pack(pady=10)

botao2 = tk.Button(janela, text="Cadastro de Horarios", command=abrir_programa2)
botao2.pack(pady=10)

botao3 = tk.Button(janela, text="Cadastro de Remédios", command=abrir_programa3)
botao3.pack(pady=10)

botao4 = tk.Button(janela, text="Sair", command=janela.quit)
botao4.pack(pady=10)


# Iniciar o loop da janela
janela.mainloop()