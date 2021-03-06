# log_cleaner

Simple python script for cleaning log files. Actually it implements linux `find` command using **_lc_props_** file.
For only testing the properties file and not applying the rules, run as `./log_cleaner.py --test`
For using a custom properties file, run as `./log_cleaner.py --props {properties_filename}`

# _lc_props_ File

Every line of the rules should be as next line:  
  
    Pattern of log files path ||| Pattern of log files ||| Number of days (log files whose modification times are older than the given number of days. This corresponds to '-mtime +' option) ||| Type of operation (delete or zip) ||| Path of compressed log file will be saved (This is used only with zip option)

# Sample Configurations

    /some/folder|||"\*.trc"|||20|||delete  
      
    /other/folder/pattern_\*|||"\*.trc"|||20|||zip|||/other/folder/archives/TEST_traces.tar.gz  
    /other/folder/archives|||"\*_\*_TEST_traces.tar.gz"|||20|||delete
