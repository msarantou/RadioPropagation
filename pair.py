#!/bin/python3



class Pair:
    first = None
    second = None

    # constructor
    def __init__(self, firstElement = None, secondElement = None):
        # reminder when giving an argument a value, it's considered as overloading
        self.first = firstElement
        self.second = secondElement

    # make_pair function
    def make_pair(self, firstElement, secondElement):
        self.first = firstElement
        self.second = secondElement

    # get function
    def get(object):
        return object.first,object.second

    # swap function:
    @staticmethod
    def swap(pairToswap):
        # assigning old values to temp variables
        newFirst = pairToswap.second
        newSecond = pairToswap.first
        # resetting original variables
        pairToswap.first = None
        pairToswap.second = None
        # setting inverted values to original variables
        pairToswap.first = newFirst
        pairToswap.second = newSecond
        # removing new variables from memory :)
        del newFirst
        del newSecond


class MyPair():
    def __init__(self,tx): 
        self.tx= tx
        self.rx= None 
        self.data = []
    
    def makepair(self,x,y):
        self.data.append(Pair(x,y))
        return True


