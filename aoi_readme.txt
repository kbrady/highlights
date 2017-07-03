Notes on the AOI configuration file:
a) The number on the top must be equal to the number of AOIs defined.
 
b) Each AOI entry for formed by 3 pieces. 
    1) The header with: AOI number, part (1 or 2), and a name for the AOI consisting of a single word. (The code does not really do anything with the name, its just for human reference) 
    2) a "begin:" followed by the first words of the AOI. It must all fit in one line
    3) an "end:" followed by the last words of the AOI. The words written down here are considered part of the AOI. It must all fit in one line

c) Any overlap between a highlight and the AOI is counted as a hit.

d) The AOIs are independent. That can have common areas but the code does not care, and processes them individually as if the others did not exist. It is therefore possible to define an AOI within an AOI. 

e) The current version does not check if there are more AOIs than the ones declared. So make sure the number on the top matches the number of AOIs. The code will ignore any excess AOIs. For example if one writes 5 on the top and then ads 7 the last 2 will be ignored. The format may be annoying but it has some coding advantages, and it will force the user to be organized and cautious. I would like any feedback on it. A future version will have some improvements on this. 

f) Each AOI defined from the file is checked to make sure it exists within the text. It will give an error message if they do not. 

g) If the delimiting words are repeated in the text such that there is ambiguity the code will ask for a longer phrase. 
 
h) If the AOI is short the easiest way is to set it up is just putting the same phrase in the "begin:" and "end:" 
 
i) The AOIs can be written in any order (it should work, although I did not test it exhaustively). 


