import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

dataframe=pd.read_csv(str(sys.argv[1]),header=None)
dataframe[0]=preprocessing.scale(dataframe[0])
dataframe[1]=preprocessing.scale(dataframe[1])

alphas=[0.001, 0.005,0.01, 0.05, 0.1, 0.5, 1, 5, 10]
n=len(dataframe)
output=[]

for alpha in alphas:
    betas=np.zeros(3)
    for iter in range(100):
        betas[0]=betas[0]-alpha/n*sum([betas[0]+betas[1]*dataframe[0][i]+betas[2]*dataframe[1][i]-dataframe[2][i] for i in range(n)])
        betas[1]=betas[1]-alpha/n*sum([(betas[0]+betas[1]*dataframe[0][i]+betas[2]*dataframe[1][i]-dataframe[2][i])*dataframe[0][i] for i in range(n)])
        betas[2]=betas[2]-alpha/n*sum([(betas[0]+betas[1]*dataframe[0][i]+betas[2]*dataframe[1][i]-dataframe[2][i])*dataframe[1][i] for i in range(n)])
    output.append(list([alpha,100,betas[0],betas[1],betas[1]]))

#personalized 
a=0.650
nb_iteration=50
betas=np.zeros(3)
for iter in range(nb_iteration):
        betas[0]=betas[0]-(a/n)*sum([betas[0]+betas[1]*dataframe[0][i]+betas[2]*dataframe[1][i]-dataframe[2][i] for i in range(n)])
        betas[1]=betas[1]-(a/n)*sum([(betas[0]+betas[1]*dataframe[0][i]+betas[2]*dataframe[1][i]-dataframe[2][i])*dataframe[0][i] for i in range(n)])
        betas[2]=betas[2]-(a/n)*sum([(betas[0]+betas[1]*dataframe[0][i]+betas[2]*dataframe[1][i]-dataframe[2][i])*dataframe[1][i] for i in range(n)])
output.append(list([a,nb_iteration,betas[0],betas[1],betas[1]]))

OutputDataframe=pd.DataFrame(output)
OutputDataframe.to_csv(sys.argv[2])



    
