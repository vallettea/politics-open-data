[Click here for associated blog post](http://ants.builders/blog/18-02-2014/predicting-abstention-rate-using-open-data.html)

To start playing do:

```
git clone https://github.com/vallettea/politics-open-data.git
cd politics-open-data
make install
```

Then

```
python plot_communes.py
```

to create the communes.png file.


You should also try to look at the interactive visualization by starting a SimpleHTTPServer

```
make webserver
```

and head over to http://localhost:8000/viz/plot.html to explore (be patient, it's quite big)!
