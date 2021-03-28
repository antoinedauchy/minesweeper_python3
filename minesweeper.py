from tkinter import *
from PIL import Image, ImageTk
from random import seed, randint

window = 0

def load_image(path):
    img = Image.open(path)
    img = img.resize((40, 40), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img


class Imgs:
    def __init__(self):
        self.zero = load_image("images/0.png")
        self.one = load_image("images/1.png")
        self.two = load_image("images/2.png")
        self.three = load_image("images/3.png")
        self.four = load_image("images/4.png")
        self.five = load_image("images/5.png")
        self.six = load_image("images/6.png")
        self.seven = load_image("images/7.png")
        self.height = load_image("images/8.png")
        self.bomb = load_image("images/bomb.png")
        self.nothing = load_image("images/nothing.png")
        self.flagged = load_image("images/flagged.png")


class Game:
    def __init__(self, width, height, nb_bombs):
        self.width = width
        self.height = height
        self.nb_bombs = nb_bombs
        self.imgs = Imgs()
        self.grid = self.__get_new_grid()
        self.canvas = Canvas(window, width=480, height=360)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.__left_click)
        self.canvas.bind("<Button-2>", self.__right_click)


    def __left_click(self, event):
        print("left_click at", event.x, event.y)


    def __right_click(self, event):
        print("right click at", event.x, event.y)
    
    
    def __put_bombs(self, grid):
        counter = 0
        seed()
        while counter < self.nb_bombs:
            while True:
                bomb_pos_x = randint(0, self.width - 1)
                bomb_pos_y = randint(0, self.height - 1)
                if grid[bomb_pos_y][bomb_pos_x] == self.imgs.nothing:
                    grid[bomb_pos_y][bomb_pos_x] = self.imgs.bomb
                    break
            counter += 1


    def __get_new_grid(self):
        grid = [0] * self.height
        y = 0
        while y < self.height:
            x = 0
            grid[y] = [0] * self.width
            while x < self.width:
                grid[y][x] = self.imgs.nothing
                x += 1
            y += 1
        self.__put_bombs(grid)
        return (grid)


    def print(self):
        y = 0
        while y < self.height:
            x = 0
            while x < self.width:
                self.canvas.create_image(x * 40 + 25, y * 40 + 25, image=self.grid[y][x])
                x += 1
            y += 1



def main():
    print("Hello World!")
    #create the window
    window = Tk()
    window.title("Minesweeper")
    window.geometry("370x370")

    game = Game(9, 9, 10)
    game.print()
    
    window.mainloop()

if __name__ == "__main__":
    main()