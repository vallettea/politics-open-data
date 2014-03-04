import pylab as plt
import numpy as np
import pandas
import random

from scipy.stats.stats import pearsonr
from sklearn.metrics import mean_squared_error
from sklearn import svm, metrics, preprocessing
from sklearn import cross_validation
from sklearn import ensemble

data = pandas.read_csv("data/cleaned_data/all_data.csv.gz", sep=",", compression="gzip")


data["REGISTERED"] = data["REGISTERED"].apply(float)
data["ABSTENTION"] = data["ABSTENTION"].apply(float)
data = data[data["REGISTERED"] > 0]
data["ABSTENTION"] = data["ABSTENTION"]/data["REGISTERED"]
data["ABSTENTION"] = (data["ABSTENTION"] - data["ABSTENTION"].min()) / (data["ABSTENTION"].max() - data["ABSTENTION"].min())


selected_features = set(data.columns)
selected_features.difference_update([
                                "DEP_CODE",
                                "COMMUNE_CODE",
                                "INSEE_CODE",
                                "POSTAL_CODE",
                                "COMMUNE_NAME",
                                "DEPARTEMENT_NAME",
                                "REGION_NAME",
                                "STATUS",
                                "REGISTERED",
                                "CENTER",
                                "SHAPE",
                                "ABSTENTION",
                                ])


to_predict = "ABSTENTION"
data = data.dropna()


print "shufling"
data.reindex(np.random.permutation(data.index))

y = data.ix[:, to_predict].astype("float64")
x = data.ix[:, selected_features].astype("float64")

print "Normalizing"
x_norm = (x - x.mean()) / (x.max() - x.min())
#remove nan columns
x_norm = x_norm.replace([np.inf, -np.inf], np.nan)
x_norm = x_norm.dropna(axis=1, how='all')
y = y.ix[x_norm.index]

print "learning"
params = {'n_estimators': 500, 'max_depth': 9, 'min_samples_split': 1,
          'learning_rate': 0.01, 'loss': 'ls', 'verbose': 1}
regressor = ensemble.GradientBoostingRegressor(**params)

# scores = cross_validation.cross_val_score(regressor, x_norm, y, cv=3)
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

size = 9*len(x_norm)/10
regressor.fit(x_norm[:size],y[:size])
expected = y[size:]
predicted = regressor.predict(x_norm[size:])
pearson = pearsonr(expected,predicted)[0]
print "Pearson coefficient: %s" % str(pearson)
print "MSE : %s" % np.sqrt(mean_squared_error(expected, predicted))


feature_importance = regressor.feature_importances_
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)[::-1]
print "100 most important features:"
i=1
for f,w in zip(x_norm.columns[sorted_idx], feature_importance[sorted_idx]):
    print "%d) %s : %d" % (i, f, w)
    i+=1
    if i > 100: break

