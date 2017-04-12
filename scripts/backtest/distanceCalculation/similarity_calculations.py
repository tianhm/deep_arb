import numpy as np
from sklearn import linear_model

def cosineDistance(vec1,vec2):
    ssq = lambda inlist: np.sqrt(np.sum([x ** 2 for x in inlist]))
    num = np.dot(vec1,np.transpose(vec2))
    den = ssq(vec1) * ssq(vec2)
    return num/den

def regressionDistance(vec1,vec2):
    regr = linear_model.LinearRegression()
    regr.fit(np.asarray(vec1).reshape(len(vec1),1),np.asarray(vec2))
    return regr.coef_

def euclidianDistance(vec1,vec2):
    return np.sqrt(np.sum([(x-y)**2 for x,y in zip(vec1,vec2)]))

def manhattanDistance(vec1,vec2):
    return np.sum([(x-y**2) for x,y in zip(vec1,vec2)])