Copyright by Gauresh Pandit
The code is written in python with system calls run from python itself. The code is expected to be run on linux as it uses linux commands internally. To search for positives a folder called 'positive' should be created with the .log files which contain the packet traces of headers. The rules for each files should be present in '<head>_rules' format which will be the rules for all the postive searches to be made for files starting with <head>.

To run the positives.py file following syntax should be used :-
py positives.py

Before running the .log files for the presumed positives should be placed in the folder named 'positive' where the code is running.
The output directory will be a directory named 'found_positives'.

This output will further be used by the next checkPositive.py program.
To run we simply do 
py checkPositive.py

Before running this program you should have run positives to generate the positives in the 'found_positives' folder.
The output will then be generated in the 'false_positives' folder which is assosiated to every type of page. (eg. 'amy', 'driod',....)