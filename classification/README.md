### This directory contains the source code to obtain our classifcation results.

The notebook...

* **paper.ipynb** contains the code for DNS fingerprinting

You can run the Jupyter Notebook inside the virtual environment with

```
pipenv run jupyter notebook
```

Note that you need to 

1. import the SQL dump and

2. specify the connection string in the config.py file of the database

... to run these notebooks.

The directory...

- **benchmarking/** contains our code to benchmark the attacks.

- **distances_resp_/** contains precalculated distances for all resolvers

- **dnslev/** contains the code for the calculation of the Damerau–Levenshtein distance

- **pickle_resp_/** contains the DNS responses for all resolvers 