from tkinter import *
from PIL import Image, ImageTk

class Game:
    def __init__(self, width, height):
        self.widht = width
        self.height = height
        self.grid = [[0] * widht] * height


    def get_new_grid():
        y = 0
        while y < height:
            x = 0
            while x < width:
                self.grid[y][x] = "nothing"
                x += 1
            y += 1

def main():
    print("Hello World!")
    #create the window
    window = Tk()
    window.title("Minesweeper")
    window.geometry("480x360")

    #create canvas
    canvas = Canvas(window, width=480, height=360)
    #canvas.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')
    #img = PhotoImage(file="images/bomb.pgm")
    #img = img.subsample(2)
    #img = img.resize((250, 250), Image.ANTIALIAS)
    #img = PhotoImage(Image("images/bomb.pgm"))
    img = Image.open("3.png")
    img = img.resize((50, 50), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    
    canvas.create_image(20, 20, anchor=NW, image=img)
    canvas.pack()

    #print_an_image
    
    
    
    
    window.mainloop()

if __name__ == "__main__":
    main()