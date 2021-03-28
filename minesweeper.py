from tkinter import *
#from PIL import ImageTk,Image


def main():
    print("Hello World!")
    #create the window
    window = Tk()
    window.title("Minesweeper")
    window.geometry("480x360")

    #create canvas
    canvas = Canvas(window, width=480, height=360)
    canvas.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')
    img = PhotoImage(file="bomb.pgm")
    canvas.create_image(20,20, anchor=NW, image=img)
    canvas.pack()

    window.mainloop()

if __name__ == "__main__":
    main()