import pygame
from pygame.locals import *
import pos

CELL_SIZE = 50
PACE = [(0,0), (65,59.5)]
DAYS_AT_MOST = 30

class posSolveClass():
    '''
    used to show the path that has been calculated as the best
    task 0: image 0,
    task 1: image 1,
    task 2: random rect graph/village/... (not sure now)
    '''
    def __init__(self, task, actions, gold):
        '''
        task(int): 0/1/2
        actions(list[str]): ['1','2',...]
        gold(list[int]): [10, 9, 8, ...]
        '''
        self.task = task
        self.act = actions
        self.window = None
        self.__gold = gold
        self.__days = DAYS_AT_MOST
        self.path = []

    def display(self):
        '''
        function of display, the main part of the class
        '''
        pygame.init()

        # set up the image and window
        pygame.display.set_caption("Task "+str(self.task))
        image = pygame.image.load('img/'+str(self.task)+".png")
        size = image.get_rect()
        self.w = size.width
        self.h = size.height
        self.window = pygame.display.set_mode([size.width, size.height])
        self.window.blit(image, (0, 0))
        
        # display the text
        self.set_text()
        
        # display the footpoint
        self.start_act()

    def start_act(self):
        '''
        function of drawing footstep, the key part of the class
        '''
        clock = pygame.time.Clock()
        
        if self.task == 0:
            last_loc = pos.POS_1_LOC['1']
            for i in self.act:

                # 2 frames in 1 second
                clock.tick(2)
                
                # update location of every step
                loc = pos.POS_1_LOC[i]
                
                if({last_loc,loc} not in self.path):
                    pygame.draw.circle(self.window, pygame.Color('green'), loc, 10)
                    pygame.draw.line(self.window, pygame.Color('green'), last_loc, loc, width = 3)
                    self.path.append({last_loc,loc})
                    print(self.path)
                else:
                    print("@@@@@@@@")
                    pygame.draw.circle(self.window, pygame.Color('red'), loc, 10)
                    pygame.draw.line(self.window, pygame.Color('red'), last_loc, loc, width = 3)
                last_loc = loc


                # update window
                pygame.display.flip()
                
                # update text
                self.__days-=1
                self.set_text()
        
        elif self.task == 1:
            heads = pos.POS_2_LOC
            last_loc = pos.POS_2_LOC['1']
            for i in self.act:
                idx = int(i)-1
                clock.tick(2)

                # find the position in the graph
                idx_col = idx%8
                idx_row = idx//8
                idx_set = idx//16
                
                # two kinds of starting position
                head = 0
                head_1 = (heads['1'][0], heads['1'][1]+idx_set*2*PACE[self.task][1])
                head_2 = (heads['2'][0], heads['2'][1]+idx_set*2*PACE[self.task][1])
                if idx_row%2 == 0:
                    head = head_1
                else:
                    head = head_2

                loc = (head[0]+idx_col*PACE[self.task][0], head[1])
                pygame.draw.circle(self.window, pygame.Color('green'), loc, 10)
                pygame.draw.line(self.window, pygame.Color('green'), last_loc, loc, width = 3)
                last_loc = loc

                pygame.display.flip()
                self.__days-=1
                self.set_text()
        # elif self.task == 2:
        #     for i in self.act:
        #         clock.tick(2)
        #         # drawGrid(self.window)
        #         pygame.draw.circle(self.window, pygame.Color('green'), (loc[0]+self.action_list[i][0], loc[1]+self.action_list[i][1]),10)
        #         loc = (loc[0]+self.action_list[i][0], loc[1]+self.action_list[i][1])
        #         pygame.display.flip()
        #         self.__gold-=20
        #         self.__days-=1
        #         self.set_text()
        else:
            raise NotImplementedError

    def set_text(self):
        '''
        set gold & days remaining in the graph
        '''        

        # background of the text
        back_surf = pygame.Surface((180,100))
        back_surf.fill(color = (255, 255, 255))
        
        # font of the texts
        font_gold = pygame.font.Font(None,32)
        font_days = pygame.font.Font(None,32)
        
        # loc of the texts
        text_loc = pos.POS_TEX_LOC[str(self.task)]
        
        # set the content of the texts
        text_gold_on_display = font_gold.render('gold: '+str(self.__gold[30-self.__days]),True,(0,0,0))
        text_days_on_display = font_days.render('days remain: '+str(self.__days),True,(255,0,0))
    
        back_surf.blit(text_days_on_display, (0, 5))
        back_surf.blit(text_gold_on_display, (30, 55))

        self.window.blit(back_surf, text_loc)

    def drawGrid(self):
        '''
        draw grid on images, basically used as a ruler
        '''
        
        # draw vertical lines
        for x in range(0, self.w, CELL_SIZE): 
            pygame.draw.line(self.window, pygame.Color('gray'), (x, 0), (x, self.h))
        
        # draw horizontal lines
        for y in range(0, self.h, CELL_SIZE):  
            pygame.draw.line(self.window, pygame.Color('gray'), (0, y), (self.w, y))
    
    def stay(self, time):
        '''
        keep the window open for required time (and shut automatically)
        '''
        clock = pygame.time.Clock()
        for i in range(time):
            clock.tick(1)
            pygame.display.flip()

# class valueIter(posSolveClass):
#     '''
#     used to show the process of the value iteration
#     *Not complished yet
#     '''
#     def __init__(self, task):
#         '''
#         almost the same as posSolveClass
#         '''
#         self.task = task

#     def display(self):
#         '''
#         display the value of every state, almost the same as above
#         '''
#         pygame.init()
#         pygame.display.set_caption("Task "+str(self.task))
#         image = pygame.image.load('img/'+str(self.task)+".png")
#         size = image.get_rect()
#         self.w = size.width
#         self.h = size.height
#         self.window = pygame.display.set_mode([size.width, size.height])
#         self.window.blit(image, (0, 0))
    
#     def update_vi(self, point, value):
#         '''
#         update value of a certain state
#         Not complished yet
#         '''
#         if self.task == 0:
#             loc = pos.POS_1_LOC[point]
#             pygame.draw.circle(self.window, pygame.Color(255,value,value), loc, 10)
#             pygame.display.flip()
#             # pass

#         elif self.task == 1:
#             heads = pos.POS_2_LOC

#             # find the position in the graph
#             idx = int(point)-1
#             idx_col = idx%8
#             idx_row = idx//8
#             idx_set = idx//16
            
#             # two kinds of starting position
#             head = 0
#             head_1 = (heads['1'][0], heads['1'][1]+idx_set*2*PACE[self.task][1])
#             head_2 = (heads['2'][0], heads['2'][1]+idx_set*2*PACE[self.task][1])
#             if idx_row%2 == 0:
#                 head = head_1
#             else:
#                 head = head_2

#             loc = (head[0]+idx_col*PACE[self.task][0], head[1])
#             pass

#         # elif self.task == 2:
#         #     pass
#         else:
#             raise NotImplementedError