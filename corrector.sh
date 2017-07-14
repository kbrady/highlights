#!/bin/bash 

file=/home/jorge/Downloads/highlights_files/full_paper_coding_for_Jorge_1_ascii.csv 
filecorrected=/home/jorge/Downloads/highlights_files/full_paper_coding_for_Jorge_1_corrected.csv
tempfile=tempfile.dat

echo start
rm $filecorrected
echo erased

sed 's/2to 1/2-to-1/' $file > $tempfile
cp $tempfile $filecorrected 

sed 's/2 to 1/2-to-1/' $filecorrected > $tempfile
cp $tempfile $filecorrected 
 
sed 's/2to1/2-to-1/' $filecorrected > $tempfile
cp $tempfile $filecorrected 


sed 's/antisuffragists/anti-suffragists/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/antisuffrage/anti-suffrage/' $filecorrected > $tempfile
cp $tempfile $filecorrected 


sed 's/at least for the President/at least for President/' $filecorrected > $tempfile
cp $tempfile $filecorrected 


sed 's/WIlson/Wilson/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/4848/48-48/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/" Pro-amendment/" (Pro-amendment/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/" Pro amendment/" (Pro-amendment/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/" (Pro amendment/" (Pro-amendment/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/(Pro amendment forces/(Pro-amendment forces/' $filecorrected > $tempfile
cp $tempfile $filecorrected 


sed 's/yellow roses;/yellow roses; /' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/yellow roses /yellow roses; /' $filecorrected > $tempfile
cp $tempfile $filecorrected 


sed 's/Wyoming Territoy/Wyoming Territory/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/run for congress back/run for congress-back/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/after the passage of the Voting/after passage of the Voting/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/32yearold/32-year-old/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/ELIZABETH CADY STANTON/Elizabeth Cady Stanton/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/SUSAN B. ANTHONY/Susan B. Anthony/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/New Jerseyallowed/New Jersey allowed/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/17000000/"17,000,000"/' $filecorrected > $tempfile
cp $tempfile $filecorrected 

sed 's/24year old/24-year-old/' $filecorrected > $tempfile
cp $tempfile $filecorrected 


sed 's/aequal/equal/' $filecorrected > $tempfile
cp $tempfile $filecorrected 













rm $tempfile

echo end

exit 0
