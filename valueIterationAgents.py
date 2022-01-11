
# valueIterationAgents.py
# -----------------------

from typing import NamedTuple
import mdp, util, graph

import collections

class ValueIterationAgent:
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.resourceconsume = util.Counter() #count how much resources have consumed
        self.runValueIteration()

        print(self.values)
        print('__________________________')
        print(self.resourceconsume)
        print('__________________________')
        print(self.getPath())


    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()  
        
        for iteration in range(self.iterations):
            value_copy = self.values.copy()
            
            for state in states:
    
                if self.mdp.isTerminal(state):
                    value_copy[state] = 2000
                else:
                    action = self.computeActionFromValues(state)
                    Q_value = self.computeQValueFromValues(state,action)
                    value_copy[state] = Q_value
            
            self.values = value_copy


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        
        T_sas_list = self.mdp.getTransitionStatesAndProbs(state, action)
        Q_value = 0
        for item in T_sas_list:
            nextState, T_sas = item
            #############Reward function conbined with resource consumption####################
            R_sas = self.mdp.getReward(state,action,nextState)
            if action == graph.Buying:
                self.resourceconsume[nextState] = 0
            else:
                if self.resourceconsume[nextState] == 0:
                    self.resourceconsume[nextState] = self.resourceconsume[state] + self.mdp.getConsume(state,action)
                else:
                    self.resourceconsume[nextState] = min(self.resourceconsume[nextState],
                                                         self.resourceconsume[state] + self.mdp.getConsume(state,action))
                if self.resourceconsume[nextState] > self.mdp.graphagent.MaxResource:
                    R_sas = -2000000
            #############Reward function conbined with resource consumption####################
                    
            Q_value += T_sas*(R_sas+self.discount*self.getValue(nextState))
        
        return Q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        
        PossibleActions = self.mdp.getPossibleActions(state)
        
        if (len(PossibleActions) == 0):
            return None
        
        Q_dict = {}
        for action in PossibleActions:
            Q_value = self.computeQValueFromValues(state,action)
            Q_dict[Q_value] = action
        return Q_dict[max(Q_dict.keys())]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
    
    def getPath(self):
        start = self.mdp.getStartState()

        path = [str(start[1])]
        state = start
        while not self.mdp.isTerminal(state) and not self.mdp.OutofDate(state):
            successor_list = self.mdp.getSuccessor(state)
            max_v = -999999999
            pivot = successor_list[0]

            for item in successor_list:
                value = self.getValue(item)
                if value >= max_v:
                    pivot = item
                    max_v = value
            path.append(str(pivot[1]))
            state = pivot

        return path
        

