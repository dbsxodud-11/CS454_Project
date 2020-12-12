import random
import math
# Read .tsp file
file_name="C:/Projects/CS454_Project/GA/att48.tsp"
testfile = open(file_name, 'r')
## Read useless lines
for i in range(3):
    testfile.readline()
D=int(testfile.readline().strip('\n').split()[-1])
for i in range(2):
    testfile.readline()
## Read position of nodes
positions = []
for i in range(D):
    x,y = testfile.readline().strip().split()[1:]
    positions.append((float(x),float(y)))
## Close input file
testfile.close()


#Solution code
'''node_list=[1,2,...,Dimension]
   position_list=position of nodes
   Dimension=number of nodes
   f=number of use of fitness function in current state
   solution structure: list of nodes which begins with 1 and ends with 1 and any other nodes appear at once [1,...,1]'''
#global node_list
#global position_list
#global Dimension
#global f #current number of fitness call
node_list=[]
for i in range(D):
    node_list.append(i+1)
position_list = positions
traffic_list = [random.uniform(1,1.5) for i in range(D)]
delivery_list = [random.randint(1, 5) for _ in range(D)]  ##should be changed


print(traffic_list)
print(delivery_list)
Dimension = D
f=0
budget=1000 #limit of number of fitness computation
def d(x,y):
    return ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5
def fitness(solution):##
    #global position_list
    global f
    d_fit=0
    t_fit=0
    s_fit=0
    for i in range(D-1):
        dist=d(position_list[solution[i]-1],position_list[solution[i+1]-1])
        traffic=traffic_list[solution[i]-1]*traffic_list[solution[i+1]-1]
        time=(dist/1000)*traffic
        d_fit+=dist
        t_fit+=time
        s_fit+=5*(math.exp(-delivery_list[solution[i+1]-1]*0.01*t_fit))
    dist = d(position_list[solution[D-1]-1],position_list[solution[D]-1])
    traffic=traffic_list[solution[D-1]-1]*traffic_list[solution[D]-1]
    time = (dist/1000)*traffic
    d_fit+=dist
    t_fit+=time
    s_fit/=(D-1)
    f+=1
    return (d_fit,t_fit,s_fit)
def rand_sol():
    #global node_list
    l=node_list.copy()[1:]
    random.shuffle(l)
    return [1]+l+[1]

def k_opt(solution,k):
    for i in range(k):
        l=solution[1:Dimension]
        s1,s2=(random.randint(0,len(l)-1),random.randint(0,len(l)-1))
        temp=l[s1]
        l[s1]=l[s2]
        l[s2]=temp
        return [1]+l+[1]
def mutate(solution,T):
    k=int(T/100)
    if k>0:
        return k_opt(solution,k)
    else:
        return solution
def dominate(fit1,fit2):
    if fit1[0]<=fit2[0] and fit1[1]<=fit2[1] and fit1[2]<=fit2[2]:
        return True
    else:
        return False
def print_fit(solution):
    fit=fitness(solution)
    print('total distance: '+str(fit[0]))
    print('total time: '+str(fit[1]))
    print('average grade: '+str(fit[2]))
    return
def MOSA(budget):
    performance_list = []
    curr_sol=rand_sol()
    curr_fit=fitness(curr_sol)
    performance_list.append(curr_fit)
    k=0
    while f<budget:
        k+=1
        T=1000/math.log(k+1)
        cand_sol=mutate(curr_sol,T)
        cand_fit=fitness(cand_sol)
        if dominate(cand_fit,curr_fit):
            curr_sol=cand_sol
            curr_fit=cand_fit
        else:
            p=1
            for i in range(3):
                delta=cand_fit[i]-curr_fit[i]
                p*=min(1,math.exp(-10*delta/T))
            if p>=random.random():
                curr_sol=cand_sol
                curr_fit=cand_fit
        performance_list.append(curr_fit)
    return curr_sol, performance_list
solution, performance = MOSA(budget)
print(performance)
# print_fit(solution)

'''
#make csv file that presents solution
import csv
f=open('solution.csv','w',newline='')
wr = csv.writer(f)
for i in range(Dimension):
    wr.writerow([str(solution[i])])
f.close()
'''
