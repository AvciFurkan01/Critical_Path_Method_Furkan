import pandas as pd
import math
import numpy as np
def yildiz(number):
    for i in range(number):
        print("*", end="")
    print("")
def yazdir_error(error_msg):
    print("Error in input file : {error_msg}")
    quit()
def alCode(data, code):
    x = 0
    flag = 0
    for i in data['TASKS']:
        if (i == code):
            flag = 1
            break
        x += 1
    if (flag == 1):
        return x
    else:
        yazdir_error("TASKS")

def ileriPass(data):
    ntask = data.shape[0]
    ES = np.zeros(ntask, dtype=np.int8)
    EF = np.zeros(ntask, dtype=np.int8)
    temp = []

    for i in range(ntask):
        if (is_nan(data['PR'][i])):
            ES[i] = 0
            try:
                EF[i] = ES[i] + data['DAYS'][i]
            except:
                yazdir_error("DAYS")

        else:
            for j in data['PR'][i]:
                index = alCode(data, j)
                temp.append(EF[index])

                if (index == i):
                    yazdir_error("PR")
                else:
                    temp.append(EF[index])

            ES[i] = max(temp)
            try:
                EF[i] = ES[i] + data['DAYS'][i]
            except:
                yazdir_error("DAYS")
        temp = []

    data['ES'] = ES
    data['EF'] = EF
    return data
def is_nan(value):
    return (not isinstance(value, str)) and math.isnan(float(value))
def backwardPass(data):
    ntask = data.shape[0]
    temp = []
    LS = np.zeros(ntask, dtype=np.int8)
    LF = np.zeros(ntask, dtype=np.int8)
    SUCCR = np.empty(ntask, dtype=object)
    for i in range(ntask - 1, -1, -1):
        if (not is_nan(data['PR'][i])):
            for j in data['PR'][i]:
                index = alCode(data, j)
                if (SUCCR[index] != None):
                    SUCCR[index] += data['TASKS'][i]
                else:
                    SUCCR[index] = data['TASKS'][i]
    data["SUCCR"] = SUCCR

    for i in range(ntask - 1, -1, -1):
        if (data['SUCCR'][i] == None):
            LF[i] = np.max(data['EF'])
            LS[i] = LF[i] - data['DAYS'][i]
        else:
            for j in data['SUCCR'][i]:
                index = alCode(data, j)
                temp.append(LS[index])

            LF[i] = min(temp)
            LS[i] = LF[i] - data['DAYS'][i]
            temp = []
    data['LS'] = LS
    data['LF'] = LF
    return data
def slack(data):
    ntask = data.shape[0]
    SLACK = np.zeros(shape=ntask, dtype=np.int8)
    CRITICAL = np.empty(shape=ntask, dtype=object)
    for i in range(ntask):
        SLACK[i] = data['LS'][i] - data['ES'][i]
        if (SLACK[i] == 0):
            CRITICAL[i] = "YES"
        else:
            CRITICAL[i] = "NO"
    data['SLACK'] = SLACK
    data['CRITICAL'] = CRITICAL

    data = data.reindex(columns=['TASKS', 'PR',
                                     'SUCCR', 'DAYS', 'ES', 'EF', 'LS', 'LF', 'SLACK', 'CRITICAL'])

    return data
def hesaplacpm(data):
    data = ileriPass(data)
    data = backwardPass(data)
    data = slack(data)
    return data
def printTask(data):
    print("\t\t\tCRITICAL PATH METHOD CALCULATOR")
    yildiz(60)
    print("\t\t\t\tMuhammed Furkan AVCI")
    yildiz(60)
    print(data)
    yildiz(60)
data = pd.read_excel("datatest3.xls")
data = hesaplacpm(data)
printTask(data)
ntask = data.shape[0]
print('--------------------Number of Scheduled Tasks-------------------- ' )
print( data.iloc[:, 0].count() )
print("----------------------First Task---------------------------------")
print("First Tasks Count: "  , len(data.iloc[0,0]), "First Tasks Name: ", data.iloc[0,0])
print("----------------------Summary---------------------------------")
cp = []
for i in range(ntask):
    if (data['SLACK'][i] == 0):
        cp.append(data['TASKS'][i])
print('The Critical path is: ' + '-'.join(cp))
tdur = 0
for i in range(ntask):
    if (data['SLACK'][i] == 0):
        tdur = tdur + data['DAYS'][i]
print('Total duration is: ' + str(tdur) + ' days')
