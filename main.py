import mdp, graph, valueIterationAgents
if __name__ == '__main__':
    mdp = mdp.MarkovDecisionProcess(graph.Q1_graph_agent)

    valueIter = valueIterationAgents.ValueIterationAgent(mdp)
    