# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 15:41:31 2018

@author: agidon20
"""
import sqlite3
import math
import re
import numpy as np
import csv
import inspect


class corr:
    def __init__(self):
        self.sum2_x = 0
        self.sum2_y = 0
        self.sum_xy = 0
        self.sum_x =  0
        self.sum_y = 0
        self.N = 0

    def step(self,x,y):
        try:
            self.sum2_x = self.sum2_x + x * x
            self.sum2_y = self.sum2_y + y * y
            self.sum_xy = self.sum_xy + x * y
            self.sum_x = self.sum_x + x
            self.sum_y = self.sum_y + y
            self.N = self.N + 1
        except:
            print('Exception in [' + inspect.stack()[0][3] + '] funciton!')            


    def finalize(self):
        try:
            Ex = self.sum_x/self.N
            Ey = self.sum_y/self.N
            Ex2 = self.sum2_x/self.N
            Ey2 = self.sum2_y/self.N
            E2x = (self.sum_x/self.N)*(self.sum_x/self.N)
            E2y = (self.sum_y/self.N)*(self.sum_y/self.N)
            s_x = (Ex2 - E2x)**0.5
            s_y = (Ey2 - E2y)**0.5
            return (self.sum_xy - self.N*Ex * Ey)/ (self.N * s_x * s_y)
        except:
            print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
    
    
    
class std:
    def __init__(self):
        self.sum2_x = 0
        self.sum_x =  0
        self.N = 0

    def step(self,x):
        try:
            self.sum2_x = self.sum2_x + x * x
            self.sum_x = self.sum_x + x
            self.N = self.N + 1
        except:
            print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
    
    def finalize(self):
        try:
            Ex2 = self.sum2_x/self.N
            E2x = (self.sum_x/self.N)*(self.sum_x/self.N)
            s = (Ex2 - E2x)
            if(s < 0):
                s = 0 #sometimes when Ex2 and E2x are very small, one can get a negative answer.
            s = s**0.5
            return s
        except:
            print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
class var:
    def __init__(self):
        self.sum2_x = 0
        self.sum_x =  0
        self.N = 0

    def step(self,x):
        try:       
            self.sum2_x = self.sum2_x + x * x
            self.sum_x = self.sum_x + x
            self.N = self.N + 1
        except:
            print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
    
    def finalize(self):
        try:
            Ex2 = self.sum2_x/self.N
            E2x = (self.sum_x/self.N)*(self.sum_x/self.N)
            return (Ex2 - E2x)
        except:
            print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
    
class stderr:
    def __init__(self):
        self.sum2_x = 0
        self.sum_x =  0
        self.N = 0


    def step(self,x):
        try:
            self.sum2_x = self.sum2_x + x * x
            self.sum_x = self.sum_x + x
            self.N = self.N + 1
        except:
           print('Exception in [' + inspect.stack()[0][3] + '] funciton!')

    def finalize(self):
        Ex2 = self.sum2_x/self.N
        E2x = (self.sum_x/self.N)*(self.sum_x/self.N)
        return (Ex2 - E2x)**0.5 / self.N**0.5

    
    
class arr_concat:
    def __init__(self):
        self.str = ""
        self.counter =  float(0.0)

    def step(self,field,fac):
        try:
            self.str = self.str + ',' + str(field + self.counter * float(fac));
            self.counter = self.counter + 1
        except:
            print('Exception in [' + inspect.stack()[0][3] + '] funciton!')

    def finalize(self):
        return self.str[1:]
    

def printf(s,*r):
    return s % r
    
    
def atan(x):
    try:
        return math.atan(x)
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')

#def abs_(x):
#    return abs(x)

def myregexp(patt,s):
    try:   
        if(s == None): return 0
        matchobj = re.search(patt,s,flags=re.IGNORECASE)
        return (not (matchobj == None))
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
def re1(patt,s):
    try:
        if(s == None): 
            return None
        matchobj = re.search(patt,s,flags=re.IGNORECASE)
        if(matchobj == None):
            return None 
        return matchobj.group(1)
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')

def arr_length(s):
    try:
        return len(np.array(list(map(float,s.split(',')))))
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')    

def arr_max(s):
    try:
        return np.max(np.array(list(map(float,s.split(',')))))
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
    
def arr_min(s):
    try:
        if s is None:
            return None
        return np.min(np.array(list(map(float,s.split(',')))))
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
        print(s)
        
def arr_avg(s):
    try:
        return np.mean(np.array(list(map(float,s.split(',')))))
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')    

def arr_slice(s,first,last):
    try:
        arr = np.array(list(map(float,s.split(','))))
        return ",".join(map(str, arr[first:last]))
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')

def arr(s,i):
    try:
        return np.array(list(map(float,s.split(','))))[i]
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')

def arr_norm(s,i):
    try:
        arr = np.array(list(map(float,s.split(','))))
        if(i==-1):
            arr /= max(arr)
        else:
            if(i==-2):
                arr /= min(arr)
            else:
                arr/= arr[i]
        return ",".join(map(str, arr))
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
        
        
def arr_mul(s,fac):
    try:    
        arr = np.array(list(map(float,s.split(','))))
        arr*= fac
        return ",".join(map(str, arr))      
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
def arr_add(s,val):
    try:
        arr = np.array(list(map(float,s.split(','))))
        arr += val
        return ",".join(map(str, arr))     
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')

def arr2_math(s1,s2,operator):
    try:
        arr1 = np.array(list(map(float,s1.split(','))))
        arr2 = np.array(list(map(float,s2.split(','))))
        if(operator == "/"):
            arr1 /= arr2
        if(operator == "*"):
            arr1 *= arr2
        if(operator == "-"):
            arr1 -= arr2
        if(operator == "+"):
            arr1 += arr2
        if(operator == "**"):
            arr1 = np.power(arr1,arr2)        
        return ",".join(map(str, arr1))    
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!') 


def arr_math(s1,val,operator):
    try:
        arr = np.array(list(map(float,s1.split(','))))
        if(operator == "/"):
            arr /= val
        if(operator == "*"):
            arr *= val
        if(operator == "-"):
            arr -= val
        if(operator == "+"):
            arr += val
        if(operator == "**"):
            arr = np.power(arr,val)
        return ",".join(map(str, arr))     
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')
        
def variable(str_var):
    try:
        if(str_var == "ra"):
        	return 202;
        if(str_var == "path"):
        	return "C:\\Users\\agidon20\\OneDrive - charite.de\\Human\\manuscript\\paper\\data\\"
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')


def arr_std(s):
    try:
        return np.std(np.array(list(map(float,s.split(',')))))
    except:
        print('Exception in [' + inspect.stack()[0][3] + '] funciton!')

def register(conn):
    conn.create_aggregate("std",1,std)
    conn.create_aggregate("stderr",1,stderr)
    conn.create_aggregate("var",1,var)
    conn.create_aggregate("corr",2,corr)
    conn.create_aggregate("arr_concat",2,arr_concat) #this is as hack as it can get
    conn.create_function("atan",1,atan)
    #conn.create_function("abs",1,abs_)
    conn.create_function("regexp",2,myregexp)
    conn.create_function("re",2,re1)
    conn.create_function("arr_min",1,arr_min)
    conn.create_function("arr_max",1,arr_max)
    conn.create_function("arr",2,arr)
    conn.create_function("arr_norm",2,arr_norm)
    conn.create_function("arr_mul",2,arr_mul)
    conn.create_function("arr_add",2,arr_add)
    conn.create_function("arr_std",2,arr_std)
    conn.create_function("arr_avg",1,arr_avg)
    conn.create_function("arr2_math",3,arr2_math)    
    conn.create_function("arr_math",3,arr_math) 
    conn.create_function("arr_length",1,arr_length)   
    conn.create_function("arr_slice",3,arr_slice)   
    conn.create_function("variable",1,variable)  
    
#    "SELECT * FROM dAP_prop_at_threshold_dist where dAP_num = 0 "

def fetch_human(sql_statement,db = "_Human_.db"):
    conn = sqlite3.connect('./database/data/' + db )
    register(conn)
    csr = conn.cursor()
    res = csr.execute(sql_statement)
    names = [d[0] for d in res.description]
    results = [dict(zip(names, row)) for row in res.fetchall()]
    csr.close()
    conn.close()
    return results

def fetch_human_table(sql_statement,table,db = "Human"):
    conn = sqlite3.connect('./database/data/' + db + '.sqlite')
    register(conn)
    csr = conn.cursor()
#    first let's take all the types in the given table
    info = csr.execute('PRAGMA TABLE_INFO(' + table + ')').fetchall()
    types = dict()
    for f in info:
        s_type = f[2].lower()
        s_type = s_type.replace('integer','int')
        s_type = s_type.replace('string','str')
        types[f[1]] =  s_type
        
    
    res = csr.execute(sql_statement)
    names = [d[0] for d in res.description]
    res = [dict(zip(names, row)) for row in res.fetchall()]
    results = dict();
    for n in names:
        results[n] = np.array([r[n] for r in res],np.dtype(types[n]))
    csr.close()
    conn.close()
    return results


def query_human(sql_statement,db = "Human.sqlite"):
    conn = sqlite3.connect('./database/data/' + db )
    register(conn)
    csr = conn.cursor()
    res = csr.execute(sql_statement)
    fields = [d[0] for d in res.description]
    data = res.fetchall()
    output = dict()
    for f in enumerate(fields):
        output[f[1]] = [ row[f[0]] for row in data]
    csr.close()
    conn.close()
    return output


def WriteDictToCSV(csv_file,csv_columns,dict_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
        csvfile.close()