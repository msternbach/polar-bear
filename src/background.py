import pygame

class Tree(pygame.sprite.Sprite):
     
     def __init__(self, x=0, y=0, width = 100, height = 100,  img_file = "assets/tree.png"):
        '''
        Initializes tree object 
        Args: x, y position of the tree, the height and width of the tree
        and the image file of the tree
        '''
        super().__init__()
        self.image = pygame.image.load(img_file) 
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y
      
     def update(self): 
         '''
         Moves the tree down the screen. 
         '''
         self.rect.y += 1

