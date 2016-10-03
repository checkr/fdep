<img src="https://github.com/checkr/fdep/raw/master/misc/fdep.png" align="right" />

fdep
====

fdep is a simple, easy-to-use, production-ready command line/library written in Python to download datasets, misc. files for your machine learning projects.

Currently it supports: AWS S3, HTTP/HTTPS

## How to install

Just type the following command line:

```
pip install fdep
```

## Installing your dependencies

Once you download a machine learning project that uses fdep, just type the following:

```
fdep install
```

## Adding more dependencies

You can add a new dataset/file dependency for your machine learning project by typing:

```
fdep add data/wordlist.txt http://www-personal.umich.edu/~jlawler/wordlist
```

NOTE: `fdep` will create the `fdep.yml` for you if you don't have it


## Uploading new datasets or trained models to production

Once you produced a new dataset for your batch trainer on production, or a trained model on local, type the following:

```
ENV=production fdep upload data/training.csv
ENV=production fdep upload data/classifier.pkl
```
