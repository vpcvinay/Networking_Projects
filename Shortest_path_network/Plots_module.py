# Module that generates graphs

import Main_module as mn 
import matplotlib.pyplot as plt

def plottings():
    Cost,Den,K = mn.plot_values()

    color = mn.val.array(['red','orange','indigo','green','blue','gold','purple'])
    plt.subplots(figsize=(15,7))
    plt.bar(K,Cost,width=0.5,color=color)
    plt.xticks(list(range(3,15)))
    for i in K:
        plt.text(i-0.25,Cost[i-K[0]]+100,str(int(Cost[i-K[0]])),fontsize=14)
        plt.text(i-0.25,Cost[i-K[0]]+400,'K = '+str(i),fontsize=14)

    plt.ylim((0,max(Cost)+800))
    plt.xlabel('$K$',fontsize=18)
    plt.ylabel('$Cost$',fontsize=18)
    plt.title('$Total \ Cost \ of \ the\ Network \ vs \ K$',fontsize=14)
    plt.savefig('Total Cost.png',dpi=300)
    
    color = mn.val.array(['red','orange','indigo','green','blue','gold','purple'])
    plt.subplots(figsize=(16,8))
    plt.bar(K,Den,width=0.5,color=color)
    plt.xticks(list(range(3,15)))
    yval = []
    for i in Den:
        t = int(i*1000)
        yval.append(t/1000)
    
    
    for i in K:
        plt.text(i-0.25,Den[i-K[0]]+0.03,str(yval[i-K[0]]),fontsize=14)
        plt.text(i-0.25,Den[i-K[0]]+0.08,'K = '+str(i),fontsize=14)
    
    plt.xlabel('$K$',fontsize=18)
    plt.ylim((0,0.95))
    plt.ylabel('$Density$',fontsize=18)
    plt.title('$Network \ Density \ of \ the\ Network \ vs \ K$',fontsize=14)
    plt.savefig('Density.png',dpi = 300)
    plt.show()
