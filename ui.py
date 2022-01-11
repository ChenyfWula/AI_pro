import pygame
from pygame.locals import *
import pos

CELL_SIZE = 50
PACE = [(0,0), (65,59.5)]
DAYS_AT_MOST = 30
COLOR_LIST = ['black']+['yellow']+[(10*i,150,10*i) for i in range(10)]

class posSolveClass():
    '''
    used to show the path that has been calculated as the best
    task 0: image 0,
    task 1: image 1,
    task 2: random rect graph/village/... (not sure now)
    '''
    def __init__(self, task, ddl, start, end, mine, actions, gold):
        '''
        task(int): 0/1/2
        start(str): '1'/'2'/...
        end(str): the same as start
        mine(str): the same as start
        resource(str): the same as start
        actions(list[str]): ['1','2',...]
        gold(list[int]): [10, 9, 8, ...]
        '''
        self.start = start
        self.end = end
        self.mine = mine
        # self.resource = resource
        self.task = task
        self.act = actions
        self.window = None
        self.__gold = gold
        self.__days = ddl
        self.path = {}
        self.positions = [pos.POS_1_LOC,pos.POS_2_LOC]

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
        
        if self.task == 0:
            start_pos = self.positions[self.task][self.start]
            end_pos = self.positions[self.task][self.end]
            mine_pos = self.positions[self.task][self.mine]
            # res_pos = self.positions[self.task][self.resource]
        elif self.task == 1:
            start_pos = self.__find_pos_in_task_1(self.start)
            end_pos = self.__find_pos_in_task_1(self.end)
            mine_pos = self.__find_pos_in_task_1(self.mine)
            # res_pos = self.find_pos_in_task_1(self.resource)
        pygame.draw.circle(self.window, pygame.Color(COLOR_LIST[0]), start_pos, 15)
        pygame.draw.circle(self.window, pygame.Color(COLOR_LIST[0]), end_pos, 15, width = 5)
        pygame.draw.polygon(self.window, pygame.Color(COLOR_LIST[0]), [(mine_pos[0],mine_pos[1]-20),(mine_pos[0]-20,mine_pos[1]+10),(mine_pos[0]+20,mine_pos[1]+10)])
        # pygame.draw.polygon(self.window, pygame.Color(COLOR_LIST[4]), [(res_pos[0]-20,res_pos[1]-20),(res_pos[0]-20,res_pos[1]+20),(res_pos[0]+20,res_pos[1]+20),(res_pos[0]+20,res_pos[1]-20)])

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
            last_loc = pos.POS_1_LOC[self.start]
            for i in self.act:
                self.set_text()
                is_mine = False

                # mining
                if int(i) < 0:
                    i = str(abs(int(i)))
                    is_mine = True

                # 2 frames in 1 second
                clock.tick(2)
                
                # update location of every step
                loc = pos.POS_1_LOC[i]
                if (last_loc != loc) or (not is_mine):
                    if((last_loc,loc) not in self.path or (loc, last_loc) not in self.path):
                        self.path[(loc,last_loc)] = 2
                        self.path[(last_loc,loc)] = 2
                    else:
                        self.path[(loc,last_loc)] += 1
                        self.path[(last_loc,loc)] += 1
                    pygame.draw.circle(self.window, pygame.Color(COLOR_LIST[2]), loc, 10)
                    pygame.draw.line(self.window, pygame.Color(COLOR_LIST[self.path[(loc,last_loc)]]), last_loc, loc, width = 5)
                elif is_mine:
                    pygame.draw.circle(self.window, pygame.Color(COLOR_LIST[1]), loc, 10)
                last_loc = loc

                # update window
                pygame.display.flip()
                
                # update text
                self.__days-=1
                
        
        elif self.task == 1:

            last_loc = self.__find_pos_in_task_1(self.start)
            for i in self.act:
                self.set_text()
                clock.tick(2)

                is_mine = False
                # mining
                if int(i) < 0:
                    i = str(abs(int(i)))
                    is_mine = True

                loc = self.__find_pos_in_task_1(i)
                if(last_loc != loc or not is_mine):
                    if((last_loc,loc) not in self.path or (loc,last_loc) not in self.path):
                        self.path[(last_loc,loc)] = 2
                        self.path[(loc,last_loc)] = 2
                    else:
                        self.path[(last_loc,loc)] += 1
                        self.path[(loc,last_loc)] += 1
                    pygame.draw.circle(self.window, pygame.Color(COLOR_LIST[2]), loc, 10)
                    pygame.draw.line(self.window, pygame.Color(COLOR_LIST[self.path[(loc,last_loc)]]), last_loc, loc, width = 5)
                elif is_mine:
                    pygame.draw.circle(self.window, pygame.Color(COLOR_LIST[1]), loc, 10)
                last_loc = loc

                pygame.display.flip()
                self.__days-=1
                
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
        # text_gold_on_display = font_gold.render('gold: '+str(self.__gold[999-self.__days]),True,(0,0,0))
        text_days_on_display = font_days.render('days remain: '+str(self.__days),True,(255,0,0))
    
        back_surf.blit(text_days_on_display, (0, 5))
        # back_surf.blit(text_gold_on_display, (30, 55))

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

    def __find_pos_in_task_1(self, state):
        idx = int(state)-1
        # find the position in the graph
        idx_col = idx%8
        idx_row = idx//8
        idx_set = idx//16
        heads = self.positions[self.task]
        # two kinds of starting position
        head = 0
        head_1 = (heads['1'][0], heads['1'][1]+idx_set*2*PACE[self.task][1])
        head_2 = (heads['2'][0], heads['2'][1]+idx_set*2*PACE[self.task][1])
        if idx_row%2 == 0:
            head = head_1
        else:
            head = head_2

        return (head[0]+idx_col*PACE[self.task][0], head[1])

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