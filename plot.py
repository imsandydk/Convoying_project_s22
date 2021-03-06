import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

CONVOY_NUMBER = 6


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

        

        distace_list = line.split(',')

        if CONVOY_NUMBER==2:
            if distace_list[-1]!= '':
                i+=1
                last_value = float(distace_list[-1])
                ys.append(last_value)
                xs.append(i)

        if CONVOY_NUMBER==4:
            total = 0
            for j in range(len(distace_list)):
                    if j>2:
                        if distace_list[j]!='':
                            total += float(distace_list[j])
            if total!=0:
                i+=1
                ys.append(total/3)
                xs.append(i)

        if CONVOY_NUMBER==6:

            total = 0
            
            for j in range(len(distace_list)):
                        if distace_list[j]!='':
                            total += float(distace_list[j])
            if total!=0:
                i+=1
                ys.append(total/5)
                xs.append(i)
    ax1.clear()
    ax1.plot(xs,ys)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
 