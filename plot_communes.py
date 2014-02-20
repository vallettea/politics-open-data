import pandas
from matplotlib import pyplot as plt
import matplotlib as mpl
from descartes import PolygonPatch
import simplejson
import numpy as np


data = pandas.read_csv("data/cleaned_data/elections.csv.gz", sep=";", compression="gzip")
data["REGISTERED"] = data["REGISTERED"].apply(float)
data["ABSTENTION"] = data["ABSTENTION"].apply(float)
data = data[data["REGISTERED"] > 0]
data["abs_prop"] = data["ABSTENTION"]/data["REGISTERED"]
data["abs_prop"] = (data["abs_prop"] - data["abs_prop"].min()) / (data["abs_prop"].max() - data["abs_prop"].min())

fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111)
patches = []
 
for geojson, abs_prop in zip(data["SHAPE"], data["abs_prop"]):
    #turn json into a python object
    poly = simplejson.loads(geojson)
    try:
        patch = PolygonPatch(poly, fc=plt.cm.autumn_r(abs_prop), ec="k", zorder=1, lw=0.3)
        ax.add_patch(patch)
    except:
        pass

ax.set_xlim(-5,10)
ax.set_ylim(40.3, 51.)
ax.axis("off")
norm = mpl.colors.Normalize(vmin = data["abs_prop"].min(), vmax = data["abs_prop"].max())
ax1 = fig.add_axes([0.1, 0.052, 0.85, 0.053])
# ax1 = fig.add_axes([0.05, 0.1, 0.055, 0.85])
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap = plt.cm.autumn_r,
                                   norm = norm,
                                   orientation = "horizontal")
cb1.set_label("Abstention (%)")

plt.savefig("communes.png")
# plt.show()