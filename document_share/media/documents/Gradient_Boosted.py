import numpy as np
from pyspark import *
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import GradientBoostedTrees
import matplotlib.pyplot as plt

sc = SparkContext()

#We'll start as usual by loading the dataset and inspecting it
path = "noheader.csv"
raw_data = sc.textFile(path)
num_data = raw_data.count()
records = raw_data.map(lambda x: x.split(","))
first = records.first()

#We will cache our dataset, since we will be reading from it many times
records.cache()


#The next step is to use our extracted mappings to convert the categorical features to binary-encoded features
#we will create a separate function to extract the decision tree feature vector, which simply converts all the values to floats and wraps them in a numpy array
def extract_features_dt(record):
    return np.array(record[2:14])


def extract_label(record):
    return float(record[-1])


data_dt = records.map(lambda r: LabeledPoint(extract_label(r), extract_features_dt(r)))

data_with_idx_dt = data_dt.zipWithIndex().map(lambda p: (p[1], p[0]))
test_dt = data_with_idx_dt.sample(False, 0.3, 42)
train_dt = data_with_idx_dt.subtractByKey(test_dt)
train_data_dt = train_dt.map(lambda p: p[1])
test_data_dt = test_dt.map(lambda p: p[1])

#we will train the Gradient Boosted tree model simply using the default arguments to the trainRegressor method
gbt_model = GradientBoostedTrees.trainRegressor(train_data_dt, categoricalFeaturesInfo={}, numIterations=10,
                                                learningRate=0.01, maxDepth=1, maxBins=2)
predictions_GBT = gbt_model.predict(test_data_dt.map(lambda x: x.features))
true_vs_predicted_dt = test_data_dt.map(lambda lp: lp.label).zip(predictions_GBT)
print("Gradient Boosted Tree prediction:" + str(true_vs_predicted_dt.take(5)))

# Error Calculating Functions
# Mean Squared Error
def squared_error(actual, pred):
    return (pred - actual) ** 2


# Mean absolute Error
def abs_error(actual, pred):
    return np.abs(pred - actual)


# Mean Log Squared Error
def squared_log_error(pred, actual):
    return (np.log(pred + 1) - np.log(actual + 1)) ** 2


# Error percenyage in Gradient Boosted Tree

mse = true_vs_predicted_dt.map(lambda p: squared_error(p[0], p[1])).mean()
mae = true_vs_predicted_dt.map(lambda p: abs_error(p[0], p[1])).mean()
rmsle = np.sqrt(true_vs_predicted_dt.map(lambda p: squared_log_error(p[0], p[1])).mean())
print("Gradient Boosted Tree - Mean Squared Error: %2.4f" % mse)
print("Gradient Boosted Tree - Mean Absolute Error: %2.4f" % mae)
print("Gradient Boosted Tree - Root Mean Squared Log Error: %2.4f" % rmsle)


#We will create a convenience function to evaluate the relevant performance metric by training the model on the training set and evaluating it on the test set for different parameter settings.
def evaluate_gbt(train, test, numIterValue, maxDepth, maxBins):
    gbt_model = GradientBoostedTrees.trainRegressor(train, categoricalFeaturesInfo={}, numIterations=numIterValue, maxDepth=maxDepth, maxBins=maxBins)
    predictions_GBT = gbt_model.predict(test.map(lambda x: x.features))
    labelsAndPredictions_GBT = test.map(lambda lp: lp.label).zip(predictions_GBT)
    rmsleGBT = np.sqrt(labelsAndPredictions_GBT.map(lambda lp: squared_log_error(lp[0], lp[1])).mean())
    return rmsleGBT


# we will plot the iteration graph
numInterationsParams = [1, 2, 3, 4, 5, 6]
metrics_gbt_iterations = [evaluate_gbt(train_data_dt, test_data_dt, param, 3, 50) for param in numInterationsParams]
print(numInterationsParams)
print(metrics_gbt_iterations)
plt.plot(numInterationsParams, metrics_gbt_iterations)
plt.xlabel('Iterations log scale')
plt.ylabel('RMSLE')
plt.title('GradientBoosted Trees - Iterators')
plt.show()

# we will plot the max bin graph
maxBinsParams = [2, 4, 6, 8, 10, 12]
metrics_gbt_maxBins = [evaluate_gbt(train_data_dt, test_data_dt, 1, 1, param) for param in maxBinsParams]
print(maxBinsParams)
print(metrics_gbt_maxBins)
plt.plot(maxBinsParams, metrics_gbt_maxBins)
plt.xlabel('Iterations log scale')
plt.ylabel('RMSLE')
plt.title('GradientBoosted Trees - Max Bins')
plt.show()

# we will plot the Max Depth graph
maxDepthParams = [1, 2, 3, 4, 5, 6]
metrics_gbt_maxDepth = [evaluate_gbt(train_data_dt, test_data_dt, 2, param, 100) for param in maxDepthParams]
print(maxDepthParams)
print(metrics_gbt_maxDepth)
plt.plot(maxDepthParams, metrics_gbt_maxDepth)
plt.xlabel('Iterations')
plt.ylabel('RMSLE')
plt.title('GradientBoosted Trees - Max Depth')
plt.show()
