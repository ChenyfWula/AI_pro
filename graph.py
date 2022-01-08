import util

Staying = 0
Mining = -1

class graphAgent:
    def __init__(self,graph,weather,start,end,vilige,mine):
        self.graph = graph
        self.weather = weather
        self.start = start
        self.end = end
        self.vilige = vilige
        self.mine = mine
    
    def getWeather(self):
        return self.weather
    
    def getNeighbour(self, loc):
        if loc == self.getEnd():
            return None
        return self.graph[loc]
    
    def getStart(self):
        return self.start
    
    def getEnd(self):
        return self.end
    
    def is_mine(self, loc):
        return loc == self.mine
    
        
#graph for question 1
Q1_graph = {
    1:[2,25],
    2:[1,3],
    3:[2,4,25],
    4:[3,5,24,25],
    5:[4,6,24],
    6:[5,7,23,24],
    7:[6,8,22],
    8:[7,9,22],
    9:[8,10,15,16,17,21,22],
    10:[9,11,13,15],
    11:[10,12,13],
    12:[11,13,14],
    13:[10,11,12,14,15],
    14:[12,13,15,16],
    15:[9,10,13,14,16],
    16:[9,14,15,17,18],
    17:[9,16,18,21],
    18:[16,17,19,20],
    19:[18,20],
    20:[18,19,21],
    21:[9,17,20,22,23,27],
    22:[7,8,9,21,23],
    23:[6,21,22,24,26],
    24:[4,5,6,23,25,26],
    25:[1,3,4,24,26],
    26:[23,24,25,27],
    27:[21,26]
}
Q1_weather = ['Hot','Hot','Sunny','Storm','Sunny','Hot','Storm','Sunny','Hot','Hot',
              'Storm','Hot','Sunny','Hot','Hot','Hot','Storm','Storm','Hot','Hot',
              'Sunny','Sunny','Hot','Sunny','Storm','Hot','Sunny','Sunny','Hot','Hot']
Q1_graph_agent = graphAgent(Q1_graph,Q1_weather,1,27,None,None)