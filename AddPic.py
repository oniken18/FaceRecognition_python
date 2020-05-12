import os
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import ttk

from PIL import Image

import FaceTrain


def start():
    root = tk.Tk()
    root.title = 'XXXX'

    imgFile = Image.open('capture-Image.jpg')
    w, h = imgFile.size

    canvas = tk.Canvas(root, width=w, height=h + 100)
    canvas.pack()

    imgFile.save('capture-Image.gif')

    newImg = PhotoImage(file='capture-Image.gif')
    canvas.create_image(w / 2, h / 2, image=newImg)

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    Names = os.listdir(THIS_FOLDER + '/recognizerFilter')

    Namelist = ttk.Combobox(canvas, value=Names)
    Namelist.current()
    Namelist.place(width=w, height=30, x=3, y=h + 10)

    def savePhoto(event):
        if Namelist.get() == "":
            messagebox.showinfo("!", "Add Person Name")
        else:
            if not Namelist.get() in Names:
                os.mkdir(THIS_FOLDER + '/recognizerFilter/' + Namelist.get())

            listOfFiles = os.listdir("recognizerFilter\\" + Namelist.get())

            imgFile1 = Image.open('capture-Image.jpg')
            imgFile1.save("recognizerFilter\\" + Namelist.get() + "\\" + str(len(listOfFiles)) + ".jpg")
            FaceTrain.start()
            root.destroy()

    butSave = tk.Button(canvas, text="save")
    butSave.place(width=50, x=20, y=h + 50)
    butSave.bind("<Button-1>", savePhoto)

    root.mainloop()
