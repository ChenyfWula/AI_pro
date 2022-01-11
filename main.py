import mdp, graph, valueIterationAgents,ui
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('-t','--task', default= 0)
    parser.add_argument('-s','--start', default= 1 )
    parser.add_argument('-e','--end', default=27)
    parser.add_argument('-m','--mine', default= 12)
    parser.add_argument('-D','--DDL',default= 30)
    parser.add_argument('-R','--Resource',default= 1200)
    
    parser.add_argument('-d','--default',default=0)
    parser.add_argument('-g','--graphic', default= 1)
    args = parser.parse_args()
    
    task = int(args.task)
    start = int(args.start)
    end = int(args.end)
    mine = int(args.mine)
    DDL = int(args.DDL)
    Resource = int(args.Resource)
    
    default = int(args.default)
    Mdp = mdp.MarkovDecisionProcess(None)
    if default == 1: #graph 1 default setting
        Mdp = mdp.MarkovDecisionProcess(graph.Q1_graph_agent_default)
    elif default == 2: #graph 2 default setting
        Mdp = mdp.MarkovDecisionProcess(graph.Q2_graph_agent_default)
    else:#user customized setting
        if task == 0:
            Q1_graph_agent = graph.graphAgent(graph.Q1_graph,graph.Q1_weather,start,end,None,mine,DDL,Resource)
            Mdp = mdp.MarkovDecisionProcess(Q1_graph_agent)
        else:
            Q2_graph_agent = graph.graphAgent(graph.Q2_graph,graph.Q2_weather,start,end,None,mine,DDL,Resource)
            Mdp = mdp.MarkovDecisionProcess(Q2_graph_agent)
            
    valueIter = valueIterationAgents.ValueIterationAgent(Mdp,0.9,100)
    graphic = int(args.graphic)
    
    if graphic == 1:
        solver = ui.posSolveClass(task, DDL, str(start), str(end), str(mine),
                                valueIter.getPath(),
                                [i for i in range(999)])
        solver.display()
        solver.stay(5) 
    else:
        print(valueIter.getPath())
            
