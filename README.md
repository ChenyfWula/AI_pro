# AI_pro
AI group project created by Yifei Chen, Yao Gu, Qichen Gao, Shuai Yan, Changming Li.

This project is based on the mathematic modeling competition in 2020b. In addition, In order to make this project closely related to AI, we have done some changes to it. Thus, it will be a little different from the original one.

# How to run the code

For this project, we have enabled it to run with command. For simply make it start, please use this command:

> python main.py
>

What's more, we allow user to set some important location in our provided map.
To change the map, please use **-t**, whose default value is 0:

>python main.py -t 1

To change the start point, please use **-s**, whose default value is 1, but remember to set it within the range. We didn't provide any check for it.
For graph 1, we can use:

> python main.py -s 5

For graph 2, we can use:

> python main.py -t 1 -s 5

To change the end point, please use **-e**, whose default value is 27, still remember to set it within the range. E.g:

> python main.py -t 1 -e 32

Mine location, deadline, resource can also be set. Using **-m, -D, -R** respectively. E.g (if you set resource to 1500 for the following case, it will be able to start mining)

> python main.py -t 1 -s 9 -e 60 -m 40 -D 25 -R 500

We provide a default setting for each of the graph by using **-d**. For graph 1, please use  **-d 1** while for graph 2, please use **-d 2**.
*Note: once you choose to use the default value, any other settings like **-e** or anything else will be useless.*

> python main.py -d 1                                     |                        python main.py -d 2

If you don not want to see our user interface, using **-g 0** to cancel it. E.g:

> python main.py -m 8 -g 0

The out put will be a list like: ['1', '25', '26', '23', '22', '8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '-8', '22', '21', '27']. For the negative number, it means that we will mining at this location. Of course, we have ensured that it is a mine.

For realistic part, we offer a random weather situation. Using **-RW 1** to switch it on. For the following two examples, you will find that they choose a totally different policy cause the random weather will greatly enhance the probability of storm. Thus, we would like to get to the exit as soon as possible. If you find the two path are the same, try it for another time cause the probability  is totally random.

> python main.py -t 1 -s 2 -e 63 -m 15 -D 25 -R 1500  -RW 1  |  python main.py -t 1 -s 2 -e 63 -m 15 -D 25 -R 1500

In the end, enjoy your time here!

# What should we install to run the project?

Basically, pygame is necessary. If you lack other things, just install what you need. Good Luck.

# What method does we use?

We use the Markov Decision Process with Value iteration to solve this problem. Using value iteration is ensured to help us find an optimal solution.