import tkinter as tk
import pyautogui
import azspc
from tkinter import filedialog
w1=tk.Tk()
screen_x,screen_y=pyautogui.size()
w1.geometry(f'{int(screen_x/4)}x{int(screen_y/4)}+{int(screen_x*1/4)}+{int(screen_y*1/4)}')
w1.title("Azur Lane 资源提取 v0")
def askdir_ipt():
    ipt_path=filedialog.askdirectory()
    e1.insert(0,ipt_path)
    print(ipt_path)

l1=tk.Label(w1,text='想解包到的文件夹:',bg='cyan')
e1=tk.Entry(w1)
b1=tk.Button(w1,text='选择文件夹',height=1,command=askdir_ipt)

b1.place(x=280,y=0)
l1.place(x=0,y=4)
e1.place(x=105,y=5)










w1.mainloop()

