import numpy as np
from collections import Counter

class LinearRegression:
    def __init__(self, fit_intercept=True, alpha=0):
        self.fit_intercept = fit_intercept
        self.alpha = alpha
        self.coefficients = None

    def fit(self, xtrain, ytrain):
        xtrain = np.array(xtrain)
        ytrain = np.array(ytrain)
        if self.fit_intercept:
            xtrain = np.c_[np.ones((xtrain.shape[0], 1)), xtrain]
        I = np.eye(xtrain.shape[1])
        self.coefficients = np.linalg.inv(xtrain.T.dot(xtrain) + self.alpha * I).dot(xtrain.T).dot(ytrain)

    def predict(self, xtest):
        xtest = np.array(xtest)
        if self.fit_intercept:
            xtest = np.c_[np.ones((xtest.shape[0], 1)), xtest]
        return xtest.dot(self.coefficients)
    
    def intercept(self):
        if self.fit_intercept:
            return self.coefficients[0]
        else:
            return None
    
    def coefs(self):
        if self.fit_intercept:
            return self.coefficients[1:]
        else:
            return self.coefficients

class LogisticRegression:
    def __init__(self,learning_rate=0.01,iterations=1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.weights = None
        self.bias = None

    def sigmoid_fn(self,z):
        return 1/(1+np.exp(-z))
    
    def fit(self,xtrain,ytrain):
        samples,features = xtrain.shape
        self.weights = np.zeros(features)
        self.bias = 0

        for _ in range(self.iterations):
            lnr_model = np.dot(xtrain,self.weights) + self.bias
            prds = self.sigmoid_fn(lnr_model)

            dw = (1/samples) * np.dot(xtrain.T,(prds - ytrain))
            db = (1/samples) * np.sum(prds - ytrain)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

    def predict(self,xtest):
        lnr_model = np.dot(xtest,self.weights) + self.bias
        prds = self.sigmoid_fn(lnr_model)
        return prds.round()
    
class KNNClassifier:
    def __init__(self,kernel=3,dist="euclidean"):
        self.kernel = kernel
        self.dist = dist

    def fit(self,xtrain,ytrain):
        self.xtrain = xtrain
        self.ytrain = ytrain

    def _predict(self,xtest):
        distances = [self._distance(xtest, xtrain) for xtrain in self.xtrain]
        k_indices = np.argsort(distances)[:self.kernel]
        k_nearest_labels = [self.ytrain[i] for i in k_indices]
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

    def _distance(self,x1,x2):
        if self.dist == 'euclidean':
            return np.sqrt(np.sum((x1 - x2) ** 2))
        elif self.dist == 'manhattan':
            return np.sum(np.abs(x1 - x2))
        else:
            raise ValueError("Invalid distance metric")
