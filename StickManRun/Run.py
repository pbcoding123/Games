from tkinter import *
import time

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("SticksMan Run")
        self.tk.resizable(False, False)
        self.tk.wm_attributes("-topmost", 1)
        self.cv = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.cv.pack()
        self.tk.update()
        self.width = 500
        self.height = 500
        self.bg = PhotoImage(file=".\\img\\background.gif")
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.cv.create_image(x*w, y*h, image=self.bg, anchor="nw")
        self.sprites = []
        self.running = True

    def mainloop(self):
        while 1:
            for sp in self.sprites:
                # if self.running and sp.className!="Door" or not self.running and sp.className=="Door":
                    sp.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


class Coords:
    def __init__(self, x1:int=0, y1:int=0, x2:int=0, y2:int=0):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


def __withx(a:Coords, b:Coords):
    if b.x1<a.x1<b.x2 or b.x1<a.x2<b.x2 or\
            a.x1<b.x1<a.x2 or a.x1<b.x2<a.x2:
        return True
    return False
def __withy(a:Coords, b:Coords):
    if b.y1<a.y1<b.y2 or b.y1<a.y2<b.y2 or\
            a.y1<b.y1<a.y2 or a.y1<b.y2<a.y2:
        return True
    return False
def colleft(a:Coords, b:Coords):
    if __withy(a, b):
        if b.x1<=a.x1<=b.x2:
            return True
    return False
def colright(a:Coords, b:Coords):
    if __withy(a, b):
        if b.x1<=a.x2<=b.x2:
            return True
    return False
def coltop(a:Coords, b:Coords):
    if __withx(a, b):
        if b.y1<=a.y1<=b.y2:
            return True
    return False
def colbottom(y:int, a:Coords, b:Coords):
    if __withx(a, b):
        calc = a.y2+y
        if b.y1<=calc<=b.y2:
            return True
    return False

class Sprite:
    def __init__(self, game):
        self.className = "Sprite"
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates

class Platform(Sprite):
    def __init__(self, game, img, x, y, width, height):
        super().__init__(game)
        self.className = "Platform"
        self.photo = img
        self.img = game.cv.create_image(x, y, image=self.photo, anchor="nw")
        self.coordinates = Coords(x, y, x+width, y+height)


class StickMan(Sprite):
    def __init__(self, game):
        super().__init__(game)
        self.className = "StickMan"
        self.images_left = [
            PhotoImage(file=".\\img\\stickL1.gif"),
            PhotoImage(file=".\\img\\stickL2.gif"),
            PhotoImage(file=".\\img\\stickL3.gif")
        ]
        self.images_right = [
            PhotoImage(file=".\\img\\stickR1.gif"),
            PhotoImage(file=".\\img\\stickR2.gif"),
            PhotoImage(file=".\\img\\stickR3.gif")
        ]
        self.img = game.cv.create_image(0, 400, image=self.images_left[0], anchor="nw")
        self.x = -2
        self.y = 0
        self.current_img = 0
        self.current_add = 1
        self.jumpG = 0.13
        self.moveG = 0.03
        self.stoped = True
        self.last_time = time.time()
        self.coordinates = Coords()
        game.cv.bind_all("<KeyPress-Left>", self.turn_left)
        game.cv.bind_all("<KeyRelease-Left>", self.stop)
        game.cv.bind_all("<KeyPress-Right>", self.turn_right)
        game.cv.bind_all("<KeyRelease-Right>", self.stop)
        game.cv.bind_all("<space>", self.jump)

    def turn_left(self, evt):
        self.x = -2
        self.stoped = False

    def turn_right(self, evt):
        self.x = 2
        self.stoped = False

    # def stop(self, evt):
    #     if self.y!=0:
    #         if self.x>0:
    #             self.x = max(0, self.x-self.moveG)
    #         else:
    #             self.x = min(0, self.x+self.moveG)
    #     else:
    #         self.x = 0

    def stop(self, evt):
        self.stoped = True

    def jump(self, evt):
        if self.y==0:
            self.y = -4

    def animate(self):
        if self.x!=0 and self.y==0:
            if time.time()-self.last_time>0.1:
                self.last_time = time.time()
                self.current_img += self.current_add
                if self.current_img>=2:
                    self.current_add = -1
                if self.current_img<=0:
                    self.current_add = 1
        if self.x<0:
            if self.y!=0:
                self.game.cv.itemconfig(self.img, image=self.images_left[2])
            else:
                self.game.cv.itemconfig(self.img, image=self.images_left[self.current_img])
        elif self.x>0:
            if self.y!=0:
                self.game.cv.itemconfig(self.img, image=self.images_right[2])
            else:
                self.game.cv.itemconfig(self.img, image=self.images_right[self.current_img])

    def coords(self):
        xy = self.game.cv.coords(self.img)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0]+27
        self.coordinates.y2 = xy[1]+30
        return self.coordinates

    def move(self):
        self.animate()
        if self.y<4:
            self.y += self.jumpG
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        if self.y>0 and co.y2>=self.game.height:
            self.y = 0
            bottom = False
        elif self.y<0 and co.y1<=0:
            self.y = 0
            top = False
        if self.x>0 and co.x2>=self.game.width:
            self.x = 0
            right = False
        elif self.x<0 and co.x1<=0:
            self.x = 0
            left = False
        for sp in self.game.sprites:
            if sp==self:
                continue
            spco = sp.coords()
            if top and self.y<0 and coltop(co, spco):
                self.y = -self.y
                top = False
            if bottom and self.y>0 and colbottom(self.y, co, spco):
                self.y = spco.y1-co.y2
                if self.y<0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y==0 and co.y2<self.game.height and colbottom(1, co, spco):
                falling = False
            if left and self.x<0 and colleft(co, spco):
                self.x = 0
                left = False
                if sp.endgame:
                    self.game.running = False
                    self.game.sprites[0].change()
            if right and self.x>0 and colright(co, spco):
                self.x = 0
                right =  False
                if sp.endgame:
                    self.game.running = False
                    self.game.sprites[0].change()
        if falling and bottom and self.y==0 and co.y2<self.game.height:
            self.y = 4
        if self.stoped:
            if self.y != 0:
                if self.x>0:
                    self.x = max(0, self.x-self.moveG)
                else:
                    self.x = min(0, self.x+self.moveG)
            else:
                self.x = 0
        self.game.cv.move(self.img, self.x, self.y)


class Door(Sprite):
    def __init__(self, game, img, x, y, width, height):
        super().__init__(game)
        self.className = "Door"
        self.photo = img
        self.img = game.cv.create_image(x, y, image=self.photo, anchor="nw")
        self.coordinates = Coords(x, y, x+(width/2), y+height)
        self.endgame = True

    def change(self):
        self.game.cv.itemconfig(self.img, image=PhotoImage(file=".\\img\\door2.gif"))
        self.className = "OpenDoor"

plat1 = ".\\img\\platform1.gif"
plat2 = ".\\img\\platform2.gif"
plat3 = ".\\img\\platform3.gif"
plat = [
    [plat3, 0, 480],
    [plat3, 150, 440],
    [plat3, 300, 400],
    [plat3, 300, 160],
    [plat2, 175, 350],
    [plat2, 50, 300],
    [plat2, 170, 120],
    [plat2, 45, 60],
    [plat1, 170, 250],
    [plat1, 230, 200],
]

g = Game()
door = Door(g, PhotoImage(file=".\\img\\door1.gif"), 48, 32, 40, 35)
g.sprites.append(door)
for p in plat:
    if p[0]==plat3:
        pt = Platform(g, PhotoImage(file=plat3), p[1], p[2], 100, 10)
        g.sprites.append(pt)
    if p[0]==plat2:
        pt = Platform(g, PhotoImage(file=plat2), p[1], p[2], 60, 10)
        g.sprites.append(pt)
    if p[0]==plat1:
        pt = Platform(g, PhotoImage(file=plat1), p[1], p[2], 30, 10)
        g.sprites.append(pt)

stick = StickMan(g)
g.sprites.append(stick)
g.mainloop()
