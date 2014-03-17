import pandas
from matplotlib import pyplot as plt
import matplotlib as mpl
from descartes import PolygonPatch
import simplejson
import numpy as np


data = pandas.read_csv("data/cleaned_data/elections.csv.gz", compression="gzip")
data["ABSTENTION"] = 100*data["ABSTENTION"].apply(float)

fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111)
patches = []
 
for geojson, abstention in zip(data["SHAPE"], data["ABSTENTION"]):
    #turn json into a python object
    poly = simplejson.loads(geojson)
    try:
        patch = PolygonPatch(poly, fc=plt.cm.autumn_r(abstention/100), ec="k", zorder=1, lw=0.3)
        ax.add_patch(patch)
    except:
        pass

ax.set_xlim(-5,10)
ax.set_ylim(40.3, 51.)
ax.axis("off")
norm = mpl.colors.Normalize(vmin = data["ABSTENTION"].min(), vmax = data["ABSTENTION"].max())
ax1 = fig.add_axes([0.1, 0.052, 0.85, 0.053])
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap = plt.cm.autumn_r,
                                   norm = norm,
                                   orientation = "horizontal")
cb1.set_label("Abstention (%)")

plt.savefig("communes.png")
# plt.show()