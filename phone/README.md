### This directory contains the Python files that were used to collect the PCAP files of the Android apps.

To get started:

1. Install Requirements from Pipfile
2. Set the parameters in your <strong> config.py </strong> file. An example is given in example_config.py.
3. Adjust the content of the **packages.txt** or the **packages_ow.txt** file. 
4. Run the **capture.py** file

You can extract the currently installed third party packages on your Android phone by typing:

```
adb shell pm list packages -3 | cut -f2 -d":"
```

You can run the capture.py file on your remote server via

```
nohup python3 capture.py &
```

Note that you might run this command in your virtual environment.