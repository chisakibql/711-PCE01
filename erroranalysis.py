import numpy as np
import matplotlib.pyplot as plt

path = "data.log"
nsamp = 15

datatlst = [[],[],[],[]]
dataalst = [[],[],[],[]]
datalabel = ["2.05", "3.03", "3.99", "5.98"]

fp = open(path, "r")
for i in range(4):
    for j in range(nsamp):
        s = fp.readline().split()
        datatlst[i].append(float(s[0]))
        dataalst[i].append(float(s[1]))
    fp.readline()
fp.close()

dataklst = [[],[],[],[]]
datarlst = [[],[],[],[]]
datakrmslst = [[],[],[],[]]

samplst = [-3.5 - 0.01*i for i in range(101)]

def lsq(n, xlst, ylst):
    sumx = np.sum(xlst)
    sumy = np.sum(ylst)
    sumx2 = np.sum([xi*xi for xi in xlst])
    sumy2 = np.sum([yi*yi for yi in ylst])
    sumxy = np.sum([xlst[i]*ylst[i] for i in range(len(xlst))])
    a = (n*sumxy-sumx*sumy)/(n*sumx2-sumx*sumx)
    b = (sumx2*sumy-sumx*sumxy)/(n*sumx2-sumx*sumx)
    r2 = pow(n*sumxy-sumx*sumy,2)/(n*sumx2-sumx*sumx)/(n*sumy2-sumy*sumy)
    sa = np.sqrt(n/(n*sumx2-sumx*sumx)*np.sum([pow(a*xlst[i]+b-ylst[i],2) for i in range(n)])/(n-2))
    print(a,b,sa,r2)
    return a, b, sa, r2

for batch in range(4):
    for kkk in range(101):
        tmplnalst = [np.log(dataalst[batch][i]-samplst[kkk]) for i in range(nsamp)]
        a, b, sa, r2 = lsq(nsamp, datatlst[batch], tmplnalst)
        dataklst[batch].append(-a)
        datarlst[batch].append(r2)
        datakrmslst[batch].append(sa)

for batch in range(4):
    plt.plot(samplst,dataklst[batch])
plt.show()

for batch in range(4):
    plt.plot(samplst,datarlst[batch])
plt.show()

for batch in range(4):
    plt.plot(samplst,datakrmslst[batch])
plt.show()

fp = open("res.log","w+")
for kkk in range(101):
    fp.write("%f,"%samplst[kkk])
    for batch in range(4):
        fp.write("%f,"%dataklst[batch][kkk])
    for batch in range(4):
        fp.write("%f,"%datakrmslst[batch][kkk])
    for batch in range(4):
        fp.write("%f,"%datarlst[batch][kkk])
    fp.write("\n")
fp.close()