import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('distance.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    i=0
    for line in lines:

        i+=1

        distace_list = line.split(',')

        if len(distace_list) > 1:

            total = 0

            for j in range(len(distace_list)):
                    
                    total += float(distace_list[j])
            
            xs.append(i)
            if total != 0:
                ys.append(total/len(distace_list))

        elif len(distace_list) == 1:
            
            if distace_list[0] != '':
                xs.append(i)
                ys.append(float(distace_list[0]))
           


        
    ax1.clear()
    ax1.plot(xs,ys)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
 