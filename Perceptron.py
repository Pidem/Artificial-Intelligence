import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

inputfile=str(sys.argv[1])
exportfile=str(sys.argv[2])

dataframe=pd.read_csv(inputfile,header=None)

weights=[0,0,0]
output=[[0,0,0]]

def classify(row,weights):
    level=dataframe[0][row]*weights[0]+dataframe[1][row]*weights[1]+weights[2]
    if level>0:
        return 1
    return -1

updating=True
while updating:
    updating=False
    for i in range(len(dataframe)):
        if dataframe[2][i]*classify(i,weights)<=0:
            weights[0]=weights[0]+dataframe[2][i]*dataframe[0][i]
            weights[1]=weights[1]+dataframe[2][i]*dataframe[1][i]
            weights[2]=weights[2]+dataframe[2][i]
            updating=True
    output.append(list(weights))

OutputDataframe=pd.DataFrame(output)
OutputDataframe.to_csv(exportfile)

#plt.scatter(dataframe[0],dataframe[1],c=dataframe[2].apply(lambda x: "red" if x==1 else "blue"),marker="o",s=50)
#x=pd.DataFrame(np.arange(min(dataframe[0]),max(dataframe[0]),0.1))
#y=x.apply(lambda u:-(weights[0]/weights[1])*u-(weights[2]/weights[1]))
#plt.plot(x,y)
#plt.show()




    