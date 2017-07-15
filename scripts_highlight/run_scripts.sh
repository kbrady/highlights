#!/bin/bash

python unicode_filter.py 
python make_standard_format.py


if [ $? -ne 0 ]
then
	# last script finished with error, stopping
	echo "Stopping execution"
  	exit 1

fi


exit 0
