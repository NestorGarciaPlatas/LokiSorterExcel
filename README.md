# LokiSorterExcel
LokisorterExcel is for visualizing the loki logs in a excel and sort the logs by Alerts Warnings Notices.

To use it install this libraries
```
pip install pandas XlsxWriter
```
Then execute the following command to execute the script.
```
python3 LokiSorter.py log_file.log
```
Extra options
```
python3 LokiSorter.py -h
```

This is an example of how will show on the excel

![image](https://github.com/NestorGarciaPlatas/LokiSorterExcel/assets/71390692/fbaa20c9-1cee-42aa-becb-2c92c44bf883)


At the end of the Excel will apper 4 sheets 

![image](https://github.com/NestorGarciaPlatas/LokiSorterExcel/assets/71390692/aa12d183-e8c5-4250-831c-1e717facf08c)


* Sheet of Logs will contain all the logs.
* Sheet of Alerts only Alerts Logs.
* Sheet of Warning only Warning Logs.
* Sheet of notices only Notices Logs.

