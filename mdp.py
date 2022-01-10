# mdp.py
# ------

import random, graph
class MarkovDecisionProcess:
    def __init__(self, graphagent):
        self.graphagent = graphagent
        
    def getSuccessor(self, state,date):
        neighbour = self.graphagent.getNeighbour(state[1])
        weather = self.graphagent.getWeather()
        
        if state[1] in self.graphagent.graph:
            successor_list = []
            if self.isTerminal(state):
                return []
            if weather[date-1] != 'Storm':
                successor_list = [(date+1,loc) for loc in neighbour]
            successor_list.append((date+1, state[1]))
            return successor_list
        else:
            raise KeyError('No successor')
        
        
    def getStates(self):
        """
        Return a list of all states in the MDP.
        Not generally possible for large MDPs.
        """
        start = self.getStartState()
        State_list = [start]
        weather_list = self.graphagent.getWeather()
        temp = State_list
        for date in range(1,len(weather_list)):
            curr_successor = []
            for state in temp:
                curr_successor.extend(self.getSuccessor(state,date))
                
            curr_successor = list(set(curr_successor))
            State_list.extend(curr_successor)
            temp = curr_successor
        
        return State_list

    def getStartState(self):
        """
        Return the start state of the MDP.
        """
        start = self.graphagent.getStart()
        return (1,start)

    def getPossibleActions(self, state):
        """
        Return list of possible actions from 'state'.
        """
        neighbour = self.graphagent.getNeighbour(state[1])
        if self.graphagent.getWeather()[state[0]-1] == 'Storm':
            return [graph.Staying, graph.Mining]
        
        if neighbour != None:
            neighbour.append(graph.Staying)
            if self.graphagent.is_mine(state[1]):
                neighbour.append(graph.Mining)
        return neighbour

    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """
        neighbour = self.graphagent.getNeighbour(state[1])
        if action in neighbour:
            return [((state[0]+1,action),1)]
        else: 
            return [((state[0]+1,state[1]),1)]
        

    def getReward(self, state, action, nextState):
        """
        Get the reward for the state, action, nextState transition.

        Not available in reinforcement learning.
        """
        weather = self.graphagent.getWeather()[state[0]-1]
        reward = 0
        if self.isTerminal(state):
            return 100 #this judgement is useless, the useful part is in valueiterationagents.py:42
        if state[0] == 30:
            return -1000
        if weather == 'Sunny':
            if action == graph.Staying:
                reward -= 95
            elif action == graph.Mining:
                reward += 715
            else:
                reward -= 190
                
        elif weather == 'Hot':
            if action == graph.Staying:
                reward -= 100
            elif action == graph.Mining:
                reward += 700
            else:
                reward -= 200
                
        elif weather == 'Storm':
            if action == graph.Staying:
                reward -= 150
            elif action == graph.Mining:
                reward += 550
        
        return reward
            

    def isTerminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """
        if state[1] == self.graphagent.getEnd():
            return True
        return False

