import pygame

class Bear(pygame.sprite.Sprite): 
     def __init__(self, x = 0 , y = 0, width = 175, height = 175, img_file = "assets/bear.png"):
         '''
         Initalizes the bear object
         args: x, y position of the bear, the height and width of the bear
         and the image file of the bear
         '''
         super().__init__()
         self.image = pygame.image.load(img_file) 
         self.image = pygame.transform.scale(self.image, (width, height))
         self.rect = self.image.get_rect()

         self.rect.x, self.rect.y = x, y
         self.dx = 0

     def update(self):
        '''
        Updates the postion of the bear with the game loop
        This function helps the bear move left and right accross the screen
        by adding to the x position of the bear
        args: no args
        '''
        self.rect.x += self.dx
                    