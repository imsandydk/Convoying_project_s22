import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

CONVOY_NUMBER = 6

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('speed.txt','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    i=0
    for line in lines:

        i+=1

        speed_list = line.split(',')

        if CONVOY_NUMBER==2:
            if speed_list[-1]!= '' and speed_list[-2]!= '':
                i+=1
                last_value = float(speed_list[-1])+ float(speed_list[-2])
                ys.append(last_value/2)
                xs.append(i)

        if CONVOY_NUMBER==4:
            total = 0
            for j in range(len(speed_list)):
                    if j>1:
                        if speed_list[j]!='':
                            total += float(speed_list[j])
            if total!=0:
                i+=1
                ys.append(total/4)
                xs.append(i)

        if CONVOY_NUMBER==6:

            total = 0
            
            for j in range(len(speed_list)):
                        if speed_list[j]!='':
                            total += float(speed_list[j])
            if total!=0:
                i+=1
                ys.append(total/6)
                xs.append(i)

    ax1.clear()
    ax1.plot(xs,ys)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
 