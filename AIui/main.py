import ui

def main():
    # an example of solution display
    # solver = ui.posSolveClass(0,
    #                         ['1','2','10','18','25'],
    #                         [i for i in range(30)])
    # solver.display()
    # solver.stay(5)
    # -------------------------------------------------------#
    # an example of vi display
    vi = ui.valueIter(0,'1',1)
    vi.display()
    vi.stay(5)

if __name__ == '__main__':
    main()