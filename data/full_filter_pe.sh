#/bin/bash

cat full.csv | cut -d, -f2,7,9,11,14  | sed 's/"//g' | sed 's/ //g' | grep -E 'exe,|tlsh' | grep -v : | grep  -v "\\.[0-9][0-9]$" |  egrep "[0-9A-F]{70}|tlsh" > full.exe.csv
