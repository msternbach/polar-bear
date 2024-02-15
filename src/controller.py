import pygame
import pygame_menu
from src.bear import Bear
import random 
from src.background import Tree
from src.points import Points

class Controller:
    def __init__(self):
        '''
         Initializes the controller and makes the state menu to start the game
         '''
        pygame.init()
        self.state = "MENU"
        

    def mainloop(self):
        '''
         Switches game screens and then runs the code for that screen
         '''
        while True:
            if self.state == "MENU":
                self.menuloop()
            elif self.state == "GAME":
                self.gameloop()
            elif self.state =="LOSS":
                self.lossloop()
            elif self.state =="WIN":
                self.winloop()

    def menuloop(self):
        '''
         Opens the menu, welcomes the player into the game, and allows them start playing
         or exit the screen
         '''
        window = pygame.display.set_mode((1200, 800))
        self.menu = pygame_menu.Menu('Welcome', 800, 600,theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input('Welcome to Cocaine Bear')
        self.menu.add.text_input('Get a score of 50 to win')
        self.menu.add.button('Play', self.gameloop)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(window)

    def gameloop(self):
        '''
         Runs the actual game itself. It starts out by displaying the background of 
         the game, and then puts the bear and tree objects on the screen. It also
         randomly puts the coke and hunter obkects on the screen. It runs a while loop
         that continues until either the bear comes in contact with the hunter or the 
         score is greater than 50. It then switches to either the loss loop or win
         loop based on whether the user won or lost the game.
         '''
        self.state = "GAME"
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        size = screen.get_size()

        x1 = (size[0] // 2)
        y1 =  (size[1])
        x2 = (size[0] // 4)
        x3 = size[0]

        forest1 = pygame.Rect(0, 0, x2, y1)
        path = pygame.Rect(x2, 0, x1, y1)
        forest2 = pygame.Rect(x1 + x2 , 0, x2, y1)
   
        pygame.draw.rect(screen, "green", forest1)
        pygame.draw.rect(screen, "brown", path)
        pygame.draw.rect(screen, "green", forest2)

        ellie_xpos = (size[0] // 2)
        ellie_ypos = (size[0] // 2) - 100

        ellie = Bear(x= ellie_xpos , y = ellie_ypos)
        ellie_group = pygame.sprite.Group(ellie)
        tree_group = pygame.sprite.Group()

        last_forest1_y = y1 // 8 
        for i in range(1, 8):
            if i % 2 == 0: 
                x = x2 // 2
            else: 
                x = x2 // 4
            y = y1 // i
            last_forest1_y = max(last_forest1_y, y)
            new_tree = Tree(x=x, y=y)
            tree_group.add(new_tree)
        last_forest2_y = y1 // 8

        for i in range(1, 8):
            if i % 2 == 0: 
                x = x3 - (x2 // 2)
            else: 
                x = x3 -  (x2 // 4)
                y = y1 // i
                last_forest2_y = max(last_forest2_y, y)
                new_tree = Tree(x=x, y=y)
                tree_group.add(new_tree)

        point_group = pygame.sprite.Group()
        point = Points(x = x1, y = 0)
        last_obs = y1 

        last_forest1_y = y1 // 8 
        for i in range(1, 8):
            if i % 2 == 0: 
                x = x2 // 2
            else: 
                x = x2 // 4
            y = y1 // i
            last_forest1_y = max(last_forest1_y, y)
            new_tree = Tree(x=x, y=y)
            tree_group.add(new_tree)
        last_forest2_y = y1 // 8

        for i in range(1, 8):
            if i % 2 == 0: 
                x = x3 - (x2 // 2)
            else: 
                x = x3 -  (x2 // 4)
                y = y1 // i
                last_forest2_y = max(last_forest2_y, y)
                new_tree = Tree(x=x, y=y)
                tree_group.add(new_tree)

        obj = ["assets/hunter.png", "assets/coke.png"]
        score = 0
        font = pygame.font.Font(None, 80)
        clock = pygame.time.Clock()  

        while self.state == "GAME":
        # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                ellie.dx = -25
            elif keys[pygame.K_RIGHT]:
                ellie.dx = 25
            else:
                ellie.dx = 0
            
            ellie_group.update() 

            screen.fill("white")
            pygame.draw.rect(screen, "green", forest1)
            pygame.draw.rect(screen, "brown", path)
            pygame.draw.rect(screen, "green", forest2)
 
            tree_group.update()
            
        
            for tree in tree_group.copy():
                if tree.rect.top > size[1]:
                    tree_group.remove(tree)
            
        
            last_forest1_y -= 5  
            last_forest2_y -= 5
            if last_forest1_y <= 0:
                new_tree = Tree(x=random.randint(0, (x2-25)), y=0)
                tree_group.add(new_tree)
                last_forest1_y = y1 // 8
            if last_forest2_y <= 0:
                new_tree = Tree(x=random.randint(x1 + x2, x3), y=0)
                tree_group.add(new_tree)
                last_forest2_y = y1 // 8
            
            point_group.update()

            obs = random.choice(obj)
            obs_x = random.randint((x2), ((x2 +x1)-100))
            last_obs -= 10 
            if last_obs <= 0: 
                new_obs = Points(x = obs_x, y = 0, img_file= obs)
                point_group.add(new_obs)
                last_obs = y1 //2 
            for p in point_group: 
                if p.img == "assets/coke.png": 
                    if pygame.sprite.collide_rect(p, ellie): 
                        score += 1
                        p.kill()
                else: 
                    if pygame.sprite.collide_rect(p, ellie):
                        self.state = "LOSS"
                        self.lossloop()
            msg = f"{score}"
            text = font.render(msg, True, "white")

            if score >= 50:
                self.state = "WIN"
                self.winloop()
            point_group.draw(screen)
            ellie_group.draw(screen)
            tree_group.draw(screen)
            screen.blit(text, (40, 40))
            pygame.display.flip()

            clock.tick(60) 



    def lossloop(self):
        '''
        Prints message on the screen saying the user lost. Another menu then comes up
        letting the user press play to play the game again or quit to exit the game
         '''
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill("red")
        font = pygame.font.Font(None, 200)
        message = font.render("YOU LOST", True, "white")
        screen.blit(message, (300,300))
        pygame.display.flip()
        pygame.time.wait(4000)
        window = pygame.display.set_mode((800, 800))
        self.menu = pygame_menu.Menu('Welcome', 500, 500,theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input('Press Play to Play Again')
        self.menu.add.button('Play', self.gameloop)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(window)
    
    def winloop(self):
        '''
        Prints message on the screen saying the user won. Another menu then comes up
        letting the user press play to play the game again or quit to exit the game
         '''
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen.fill("black")
        font = pygame.font.Font(None, 200)
        message = font.render("YOU WON!!!", True, "white")
        screen.blit(message, (300,300))
        pygame.display.flip()
        pygame.time.wait(4000)
        window = pygame.display.set_mode((800, 800))
        self.menu = pygame_menu.Menu('Welcome', 500, 500,theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input('Press Play to Play Again')
        self.menu.add.button('Play', self.gameloop)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(window)

