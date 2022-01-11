import mdp, graph, valueIterationAgents,ui
if __name__ == '__main__':
    mdp = mdp.MarkovDecisionProcess(graph.Q1_graph_agent_default)

    valueIter = valueIterationAgents.ValueIterationAgent(mdp,0.9,50)
    solver = ui.posSolveClass(0,
                            valueIter.getPath(),
                            [i for i in range(30)])
    solver.display()
    solver.stay(5)