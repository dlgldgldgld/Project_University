# -*- 0coding: utf-8 -*-
"""
Back-Propagation Neural Networks Written in Python.

This is a slightly different version of this http://arctrix.com/nas/python/bpnn.py
"""
import math
import random
import re
import glob
import string

random.seed(0)
File = open('C:\Users\HanSoo Shin\Desktop\input_Node.txt', 'r')
File2 = glob.glob('C:\Users\HanSoo Shin\Desktop\Data(0)\Tr\*.txt')
File3 = glob.glob('C:\Users\HanSoo Shin\Desktop\Data(0)\Te\*.txt')
write_file = open('C:\Users\HanSoo Shin\Desktop\Answer_0or1.txt','w')
pre_error = 10000.0

pattern = re.compile("[^/]*[/][^+]*[+]{0,1}") # Word Pattern
p = re.compile('[^/]*') # split pattern
rbclr = re.compile('\d{7}') # category Pattern
Input_Node = []



# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in xrange(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2

class NN:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1 # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # set them to random vaules
        for i in xrange(self.ni):
            for j in xrange(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in xrange(self.nh):
            for k in xrange(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError('wrong number of inputs')

        # input activations
        for i in xrange(self.ni-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ai[i] = inputs[i]

        # hidden activations
        for j in xrange(self.nh):
            sum = 0.0
            for i in xrange(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)

        # output activations
        for k in xrange(self.no):
            sum = 0.0
            for j in xrange(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in xrange(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in xrange(self.nh):
            error = 0.0
            for k in xrange(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in xrange(self.nh):
            for k in xrange(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                #print N*change, M*self.co[j][k]

        # update input weights
        for i in xrange(self.ni):
            for j in xrange(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in xrange(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, patterns,a,Moon):
        i = 0
        for p in patterns:
            if  p[1].index(max(p[1])) == self.update(p[0]).index(max(self.update(p[0]))):
                a[p[1].index(max(p[1]))][self.update(p[0]).index(max(self.update(p[0])))] += 1
                i += 1
            else :
                a[p[1].index(max(p[1]))][self.update(p[0]).index(max(self.update(p[0])))] += 1

            write_file.write(str(p[0]))
            write_file.write('->')
            write_file.write(str(self.update(p[0])))
            write_file.write("\n")

        if Moon == 2:
            pp = float(i)/len(File2)
        else :
            pp = float(i)/len(File3)
        write_file.write('correct Answer : ')
        write_file.write(str(i))
        write_file.write(',All Counter : ')
        if Moon == 2:
            write_file.write(str(len(File2)))
        else :
            write_file.write(str(len(File3)))
        write_file.write(',pp :')
        write_file.write(str(pp))
        write_file.write('\n')
        write_file.write(str(a))
        write_file.write("\n")

    def weights(self):
        write_file.write('Input weights:')
        for i in xrange(self.ni):
            write_file.write(str(self.wi[i]))
        write_file.write()
        write_file.write('Output weights:')
        for j in xrange(self.nh):
            write_file.write(str(self.wo[j]))

    def train(self, patterns, iterations=50, N=0.1, M=0.1):
        # N: learning rate
        # M: momentum factor
        global pre_error

        for i in xrange(iterations):
            print pre_error
            error = 0.0
            print i
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if i % 10 == 0:
                print('error %-.5f' % error)

            # if Pre_Error - Error <= 0.1 and error <1.0  ==> Train Quit
            if abs(pre_error - error) <= 0.1  and error < 1.0:
                break
            pre_error = error



##
def WordProcessing(check,Input_Node_idx) :
    a = p.findall(check)
    try :
        if a[0] != '\n':
            if a[2][0] == 'N' or a[2][0] == 'V':
                if Input_Node.count(a[0]+'\n') >= 1:
                    #Input_Node_idx[Input_Node.index(a[0]+'\n')] += 1
                    #Per_ Count
                    Input_Node_idx[Input_Node.index(a[0]+'\n')] = 1
                    #1 or 0
    except IndexError as e :
        pass

# Systax -> Word
def SyntaxProcessing(data,Input_Node_idx):
    neep = data.split()
    for i in neep :
        FuckData = pattern.findall(i)
        for z in FuckData:
            WordProcessing(z,Input_Node_idx)

def R_Input_idx(a):
    return a

def R_Answer_idx(a):
    return a
##
def demo():
    pat = []
    pat_Te = []
    a = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    z=0
    n = NN(1000, 2, 5)
    # Teach network XOR function


    # Call Input_layer Node
    while True:
        data = File.readline()
        if not data : break
        Input_Node.append(data)

    # Learning MLP through Tr Data
    for temp in File2:
        Input_Node_idx = []
        Input_Answer = []

        for i in range(0,1000):
            Input_Node_idx.append(0)

        for i in range(0,5):
            Input_Answer.append(0)
        for i in range(0,1000):
             Input_Node_idx[i]=0

        DocNumber = rbclr.findall(temp)

        for i in range(0,5):
            Input_Answer[i] = 0
        Input_Answer[int(DocNumber[0][2]) - 1 ] = 1

        try:
            f = open(temp,'r')
        except IOError as e :
            pass
        else :
            while True:
                data = f.readline()
                if not data: break
                try:
                    SyntaxProcessing(data,Input_Node_idx)
                except UnicodeDecodeError :
                    pass
            f.close()
        pat.append([R_Input_idx(Input_Node_idx), R_Input_idx(Input_Answer)])

    random.shuffle(pat)

    n.train(pat)
    n.test(pat,a,2)
    # n.weights()


    # Test MLP through Te Data

    for temp in File3:
        Input_Node_idx = []
        Input_Answer = []

        for i in range(0,1000):
            Input_Node_idx.append(0)

        for i in range(0,5):
            Input_Answer.append(0)
        for i in range(0,1000):
            Input_Node_idx[i]=0

        DocNumber = rbclr.findall(temp)

        for i in range(0,5):
            Input_Answer[i] = 0
        Input_Answer[int(DocNumber[0][2]) - 1 ] = 1

        try:
            f = open(temp,'r')
        except IOError as e :
            pass
        else :
            while True:
                data = f.readline()
                if not data: break
                try:
                    SyntaxProcessing(data,Input_Node_idx)
                except UnicodeDecodeError :
                    pass
            f.close()
        pat_Te.append([R_Input_idx(Input_Node_idx), R_Input_idx(Input_Answer)])

    b = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

    n.test(pat_Te,b,3)

if __name__ == '__main__':
    demo()