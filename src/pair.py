"""

 DESCRIPTION
 The class Pair receives two values as input and creates an object which consists of those two 
 values, providing a way to store two heterogeneous objects as a single unit.
 The class MyPair creates an object which consists of the Tx's or Rx's name as well, and the 
 former set of values that corresponds to the aforementioned Tx or to the a pair of Tx-Rx. 
 
 Class MyPair
 Inputs:
   tx:                  The Tx's name (e.g. Tx1, Tx2 etc)
   rx:                  The Rx's name (e.g. Rx1, Rx2 etc)

 Outputs:
   * Function makepair(x,y)
     This function receives as inputs two values: x (firstElement) and y (secondElement) 
        data:           An array that stores for each object the pair of x,y. 
        
"""



class Pair:
    first = None
    second = None

    # constructor
    def __init__(self,firstElement = None,secondElement = None):
        self.first = firstElement
        self.second = secondElement

    # get function --> provides access to the data
    def get(object):
        return object.first,object.second


class MyPair():

    def __init__(self,tx,rx): 
        self.tx= tx
        self.rx= rx
        self.data = []
    
    def makepair(self,x,y):
        self.data.append(Pair(x,y))
        return True


