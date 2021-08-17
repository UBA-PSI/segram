## How Private is Android's Private DNS Setting? Identifying Apps by Encrypted DNS Traffic

This repository contains the source code and datasets for the paper "How Private is Android's Private DNS Setting? Identifying Apps by Encrypted DNS Traffic". Our paper will appear in the Proceedings of The 16th International Conference on Availability, Reliability and Security (ARES 2021).

A preprint is available on arxiv: https://arxiv.org/abs/2106.14058

The paper is now also available in the digital library of ACM (https://doi.org/10.1145/3465481.3465764).

The suggested citation by ACM Ref looks as follows:

```
Michael Mühlhauser, Henning Pridöhl, and Dominik Herrmann. 2021. How Private is Android’s Private DNS Setting? Identifying Apps by Encrypted DNS Traffic. In The 16th International Conference on Availability, Reliability and Security (ARES 2021). Association for Computing Machinery, New York, NY, USA, Article 14, 1–10. DOI:https://doi.org/10.1145/3465481.3465764
```

#### The directory...

* <strong>classification/</strong> contains Jupyter Notebooks to reproduce the results.

* <strong>data/</strong> contains the SQL Dump of the PostgreSQL database (only the DoT/DoH data)

* <strong>database/</strong> contains the database configuration for DNS fingerprinting and the script that is used to parse the PCAP files

* <strong>phone/</strong> contains the implementation that was used to instrument the Android smartphone

* <strong>tests/</strong> containts some tests to check parts of the code

## Classification Results

#### 1. Install Requirements

To get started install the packages from the pipfile.

```
pipenv install
```

#### 2. Load the SQL Dump:

2.1 Install PostgreSQL

```
sudo apt install postgresql postgresql-client
```

2.2 Set Password for User postgres

```
sudo -u postgres psql 
```

```
\password postgres  
```

2.3 Create User 

```
sudo -u postgres createuser -P -d USERNAME 
```

2.4 Create Database

```
sudo -u postgres createdb -O USERNAME DATABASENAME 
```

2.5 Load Database from SQL Dump

```
psql DATABASENAME < ./data/encdnsdata.sql 
```

#### 3. Connect to your Database.

* create the <strong> config.py </strong> file in the <strong>database/</strong> directory. 
  An example is given here and in the example_config.py file. 

```
DATABASE_URI = 'postgresql://username:password@localhost:5432/dbname'
```

#### 4. Run the Jupyter Notebook inside the Virtual Environment

```
pipenv run jupyter notebook
```
