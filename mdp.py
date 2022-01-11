# mdp.py
# ------

import random, graph
class MarkovDecisionProcess:
    def __init__(self, graphagent):
        self.graphagent = graphagent
        
    def getSuccessor(self, state):
        neighbour = self.graphagent.getNeighbour(abs(state[1]))
        #neighbour = list(set(neighbour))

        date = state[0]
        if abs(state[1]) in self.graphagent.graph.keys():

            if self.isTerminal(state):
                return []
        
            successor_list = [(date+1,loc) for loc in neighbour]
            successor_list.append((date+1, state[1]))
            
            if self.graphagent.is_mine(abs(state[1])) or self.graphagent.is_vilige(abs(state[1])):
                successor_list.append((date+1, -abs(state[1])))
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
                curr_successor.extend(self.getSuccessor(state))
                
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
        neighbour = self.graphagent.getNeighbour(abs(state[1])).copy()
        
        if neighbour != None:
            neighbour.append(graph.Staying)
            if self.graphagent.is_mine(abs(state[1])):
                neighbour.append(graph.Mining)
            if self.graphagent.is_vilige(abs(state[1])):
                neighbour.append(graph.Buying)
        return neighbour

    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """
        weather = self.graphagent.getWeather()[state[0]-1]
        Sunny_prob = weather[0]
        Hot_prob = weather[1]
        Storm_prob = weather[2]
        
        if action > 0:
            nextdate = state[0]+1
            return [((nextdate,action),Sunny_prob),((nextdate,action),Hot_prob),((nextdate,abs(state[1])),Storm_prob)]
        elif action < 0: 
            return [((state[0]+1,-abs(state[1])),Sunny_prob),((state[0]+1,-abs(state[1])),Hot_prob),((state[0]+1,-abs(state[1])),Storm_prob)]
        return [((state[0]+1,abs(state[1])),Sunny_prob),((state[0]+1,abs(state[1])),Hot_prob),((state[0]+1,abs(state[1])),Storm_prob)]
        

    def getReward(self, state,action, weather):
        """
        Get the reward for the state, action, nextState transition.

        Not available in reinforcement learning.
        """
        reward = 0
        if self.isTerminal(state):
            return 100 #this judgement is useless, the useful part is in valueiterationagents.py:42
        if state[0] >= self.graphagent.getDDL():
            return -2000000
        
        if weather == 0:#'Sunny':
            if action == graph.Staying or action == graph.Buying:
                reward -= 95
            elif action == graph.Mining:
                reward += 715
            else:
                reward -= 190
                
        elif weather == 1:#'Hot':
            if action == graph.Staying or action == graph.Buying:
                reward -= 100
            elif action == graph.Mining:
                reward += 700
            else:
                reward -= 200
                
        elif weather == 2:#'Storm':
            if action == graph.Staying or action == graph.Buying:
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
        if abs(state[1]) == self.graphagent.getEnd():
            return True
        return False
    
    def getConsume(self,state,action,weather):
        
        if weather == 0:#'Sunny':
            if action == graph.Staying:
                return 29
            elif action == graph.Mining:
                return 87
            else:
                return 58
                
        elif weather == 1:#'Hot':
            if action == graph.Staying:
                return 36
            elif action == graph.Mining:
                return 108
            else:
                return 72
                
        elif weather == 2:#'Storm':
            if action == graph.Staying:
                return 50
            elif action == graph.Mining:
                return 150
        
        return 0
        
        
    def OutofDate(self,state):
        if state[0] > self.graphagent.getDDL():
            return True
        return False

