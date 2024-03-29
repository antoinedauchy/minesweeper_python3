# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    minesweeper.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: adauchy <adauchy@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/26 18:42:23 by adauchy           #+#    #+#              #
#    Updated: 2021/03/29 23:08:27 by adauchy          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from tkinter import *
from PIL import Image, ImageTk
from random import seed, randint

window = 0

def load_image(path):
    img = Image.open(path)
    img = img.resize((40, 40), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img


class Block:
    def __init__(self, img, discovered, flagged):
        self.img = img
        self.discovered = discovered
        self.flagged = flagged

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
        self.canvas = Canvas(window, width=370, height=370)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.__left_click)
        self.canvas.bind("<Button-2>", self.__right_click)
        self.__lost_game = False
        self.__won_game = False


    def __recursive_exploration(self, x, y):
        if self.grid[y][x].discovered == True:
            return
        self.grid[y][x].discovered = True
        self.grid[y][x].flagged = False
        if self.grid[y][x].img != self.imgs.zero:
            return
        if y - 1 >= 0 and x - 1 >= 0:
            self.__recursive_exploration(x - 1, y - 1)
        if y - 1 >= 0:
            self.__recursive_exploration(x, y - 1)
        if y - 1 >= 0 and x + 1 < self.width:
            self.__recursive_exploration(x + 1, y - 1)
        if x - 1 >= 0:
            self.__recursive_exploration(x - 1, y)
        if x + 1 < self.width:
            self.__recursive_exploration(x + 1, y)
        if y + 1 < self.height and x - 1 >= 0:
            self.__recursive_exploration(x - 1, y + 1)
        if y + 1 < self.height:
            self.__recursive_exploration(x, y + 1)
        if y + 1 < self.height and x + 1 < self.width:
            self.__recursive_exploration(x + 1, y + 1)


    def __print_lost_game(self):
        self.canvas.delete("all")
        y = 0
        while y < self.height:
            x = 0
            while x < self.width:
                self.canvas.create_image(x * 40 + 25, y * 40 + 25, image=self.grid[y][x].img)
                x += 1
            y += 1
        self.canvas.create_text(183, 185, text="Game Over", font=("Helvetica", "56"), fill="white")
        self.canvas.create_text(187, 185, text="Game Over", font=("Helvetica", "56"), fill="white")
        self.canvas.create_text(185, 183, text="Game Over", font=("Helvetica", "56"), fill="white")
        self.canvas.create_text(185, 187, text="Game Over", font=("Helvetica", "56"), fill="white")
        self.canvas.create_text(185, 185, text="Game Over", font=("Helvetica", "56"), fill="#900000")


    def __check_win(self):
        y = 0
        while y < self.height:
            x = 0
            while x < self.width:
                if self.grid[y][x].img != self.imgs.bomb and self.grid[y][x].discovered == False:
                    return False
                x += 1
            y += 1
        self.__won_game = True
        return True


    def __print_won_game(self):
        self.print()
        self.canvas.create_text(183, 185, text="You Win", font=("Helvetica", "60"), fill="white")
        self.canvas.create_text(187, 185, text="You Win", font=("Helvetica", "60"), fill="white")
        self.canvas.create_text(185, 183, text="You Win", font=("Helvetica", "60"), fill="white")
        self.canvas.create_text(185, 187, text="You Win", font=("Helvetica", "60"), fill="white")
        self.canvas.create_text(185, 185, text="You Win", font=("Helvetica", "60"), fill="#00B000")



    def __left_click(self, event):
        if self.__lost_game == True or self.__won_game == True:
            self.__lost_game = self.__won_game = False
            self.grid = self.__get_new_grid()
            self.print()
            return
        x_block = (int)(((event.x) - 5) / 40)
        y_block = (int)(((event.y) - 5) / 40)
        if x_block < 0 or x_block >= self.width or y_block < 0 or y_block >= self.height:
            return
        if self.grid[y_block][x_block].flagged == False and self.grid[y_block][x_block].img == self.imgs.zero:
            self.__recursive_exploration(x_block, y_block)
        elif self.grid[y_block][x_block].flagged == False and self.grid[y_block][x_block].img == self.imgs.bomb:
            self.__lost_game = 1
        elif self.grid[y_block][x_block].flagged == False:
            self.grid[y_block][x_block].discovered = True
        if self.__lost_game == 1:
            self.__print_lost_game()
        elif self.__check_win() == True:
            self.__print_won_game()
        else:
            self.print()


    def __right_click(self, event):
        if self.__lost_game == True or self.__won_game == True:
            return
        x_block = (int)(((event.x) - 5) / 40)
        y_block = (int)(((event.y) - 5) / 40)
        if x_block < 0 or x_block >= self.width or y_block < 0 or y_block >= self.height:
            return
        if self.grid[y_block][x_block].flagged == False and self.grid[y_block][x_block].discovered == False:
            self.grid[y_block][x_block].flagged = True
        elif self.grid[y_block][x_block].flagged == True:
            self.grid[y_block][x_block].flagged = False
        self.print()



    def __count_bombs(self, grid, y, x):
        nb_bombs = 0
        if y - 1 >= 0 and x - 1 >= 0 and grid[y - 1][x - 1].img == self.imgs.bomb:
            nb_bombs += 1
        if y - 1 >= 0 and grid[y - 1][x].img == self.imgs.bomb:
            nb_bombs += 1
        if y - 1 >= 0 and x + 1 < self.width and grid[y - 1][x + 1].img == self.imgs.bomb:
            nb_bombs += 1
        if x - 1 >= 0 and grid[y][x - 1].img == self.imgs.bomb:
            nb_bombs += 1
        if x + 1 < self.width and grid[y][x + 1].img == self.imgs.bomb:
            nb_bombs += 1
        if y + 1 < self.height and x - 1 >= 0 and grid[y + 1][x - 1].img == self.imgs.bomb:
            nb_bombs += 1
        if y + 1 < self.height and grid[y + 1][x].img == self.imgs.bomb:
            nb_bombs += 1
        if y + 1 < self.height and x + 1 < self.width and grid[y + 1][x + 1].img == self.imgs.bomb:
            nb_bombs += 1
        return nb_bombs
    
    def __put_numbers(self, grid):
        y = 0
        tab_numbers = [self.imgs.zero, self.imgs.one, self.imgs.two, self.imgs.three, self.imgs.four,
        self.imgs.five, self.imgs.six, self.imgs.seven, self.imgs.height]
        while y < self.height:
            x = 0
            while x < self.width:
                if grid[y][x].img != self.imgs.bomb:
                    grid[y][x].img = tab_numbers[self.__count_bombs(grid, y, x)]
                x += 1
            y += 1

    def __put_bombs(self, grid):
        counter = 0
        seed()
        while counter < self.nb_bombs:
            while True:
                bomb_pos_x = randint(0, self.width - 1)
                bomb_pos_y = randint(0, self.height - 1)
                if grid[bomb_pos_y][bomb_pos_x].img == self.imgs.nothing:
                    grid[bomb_pos_y][bomb_pos_x].img = self.imgs.bomb
                    break
            counter += 1


    def __get_new_grid(self):
        grid = [0] * self.height
        y = 0
        while y < self.height:
            x = 0
            grid[y] = [0] * self.width
            while x < self.width:
                grid[y][x] = Block(self.imgs.nothing, False, False)
                x += 1
            y += 1
        self.__put_bombs(grid)
        self.__put_numbers(grid)
        return (grid)


    def print(self):
        self.canvas.delete("all")
        y = 0
        while y < self.height:
            x = 0
            while x < self.width:
                if self.grid[y][x].flagged == True:
                    self.canvas.create_image(x * 40 + 25, y * 40 + 25, image=self.imgs.flagged)
                elif self.grid[y][x].discovered == True:
                    self.canvas.create_image(x * 40 + 25, y * 40 + 25, image=self.grid[y][x].img)
                else:
                    self.canvas.create_image(x * 40 + 25, y * 40 + 25, image=self.imgs.nothing)
                x += 1
            y += 1



def main():
    print("Minesweeper")
    window = Tk()
    window.title("Minesweeper")
    window.geometry("370x370")
    window.resizable(False, False)

    game = Game(9, 9, 10)
    game.print()
    
    window.mainloop()

if __name__ == "__main__":
    main()
