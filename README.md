<img src="https://github.com/checkr/fdep/raw/master/misc/fdep.png" align="right" />

<h1>
  fdep
  &nbsp;
  <a href="https://circleci.com/gh/checkr/fdep/tree/master">
    <img src="https://circleci.com/gh/checkr/fdep/tree/master.svg?style=shield&circle-token=290f477815cb38bc3b464699362e6cae6880823f" alt="CircleCI">
  </a>
  <a href="https://codeclimate.com/repos/57f44216f08b620069002513/coverage">
    <img src="https://codeclimate.com/repos/57f44216f08b620069002513/badges/c7be057ea63371be9b4d/coverage.svg" alt="Test Coverage">
  </a>
  <a href="https://codeclimate.com/repos/57f44216f08b620069002513/feed">
    <img src="https://codeclimate.com/repos/57f44216f08b620069002513/badges/c7be057ea63371be9b4d/gpa.svg" alt="Code Climate">
  </a>
</h1>

fdep is a simple, easy-to-use, production-ready command line/library written in Python to download datasets, misc. files for your machine learning projects.

<table>
  <tr>
    <td>Supported versions</td>
    <td>Python 2.7, 3.0+, PyPy</td>
  </tr>
  <tr>
    <td>Available backends</td>
    <td>AWS S3, HTTP/HTTPS</td>
  </tr>
</table>

```
Usage: fdep <command> <arguments>

fdep installs miscellaneous file dependencies. e.g. datasets, etc.

  help                            Print this helpful message
  version                         Print the currently installed version
  init <envs...>                  Create fdep.yml with specified
                                  environments
  install                         Install dependencies for the project
  upload <local path>             Upload a file to the storage
  commit <local path>             Upload a file to the storage with a versioning tag
  add <local path> <remote path> [<version>]
                                  Add a new dependency to the project
  rm <local path>                 Remove a dependency in the project
```

## How to install

Just type the following command line:

```
pip install fdep
```

Or, you can install fdep from source:

```
git clone git@github.com:checkr/fdep.git
cd fdep
python setup.py install
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

NOTE: `fdep init` will create the `fdep.yml` for you if you don't have it


## Uploading new datasets or trained models to production

Once you produced a new dataset for your batch trainer on production, or a trained model on local, type the following:

```
ENV=production fdep upload data/training.csv
ENV=production fdep upload data/classifier.pkl
```

Or, if you want to tie it to your VCS, you can version control the files with the following:

```
ENV=production fdep commit data/training.csv
ENV=production fdep commit data/classifier.pkl
```

This will upload files with a versioning postfix to your backend. You can now commit your changed fdep.yml.


## FAQ

> Q. How do I set up my S3 backend?

You can set up [aws-cli](https://aws.amazon.com/cli/) on your machine, or use the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

> Q. I uploaded my newly changed file, and my old program that relied on the previous file now fails. How can I solve this problem?

You can use `fdep commit <file name>` to do a simple versioning. It'll append a version number to the filename, so in the backend, it's all separate files. Also, the fdep.yml file will be updated, so your version control software can help you pick up the right version.

> Q. Hey, I found a bug. How can I contribute to this project?

fdep is in its early stage, and there are so many things to be done! Please fork this Github project and make a pull request. Any feedback is appreciated!
