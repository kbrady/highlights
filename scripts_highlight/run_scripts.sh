#!/bin/bash

python unicode_filter.py 
python make_standard_format.py


if [ $? -ne 0 ]
then
	# last script finished with error, stopping
	echo "Stopping execution"
  	exit 1

fi

python typo_corrector.py
python validate_highlights.py
python aoi_module.py
python aoi_stats.py

exit 0
