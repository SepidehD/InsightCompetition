About the codes:

I devided the code in two sections that are available in ./src folder:
first:To calculate the medianvals by zipcode.
Second:To calculate the medianvals by date.

I ran both codes using the ./input/itcont.txt and the results are saved in the ./output folder.

Unfortunately, I could not use the run_tests.shp that you have provided for us to check the results.
I get this error: no module named pandas. I have to mention that I tried many ways to solve this probelm
but finally I got the same error. I installed the pandas again using pip, I uninstalled and installed pandas,
I checked all the dependencies and etc.

My results of two codes that are saved in txt files show that the codes work well and the structure and contents of the results are 
meet your requirements.


The summary of the codes:

I start to summerize the medianval_by_date because I belive I used a better approach writting this code. It is very simple and fast.
I loaded and prepared the data frame based on the requirements. For example, I dropped rows which have null value in recipiant id, zipcode 
and the amount of transaction. I did not used the rows which contain information in "OTHER_ID" because we are interested
only in individual contributions. 
After preparing data, I used two functions.First function output is the list of dates of transcations corresponding to each recipiant.
The second function, in somehow, gorups the recipiant id and date of transactions and calculate the mean, sum , and number of transcation
for each gorup. 
Based on the requirements of the question, the final code contains following fileds:

    recipient of the contribution (or CMTE_ID from the input file)
    5-digit zip code of the contributor (or the first five characters of the ZIP_CODE field from the input file)
    running median of contributions received by recipient from the contributor's zip code streamed in so far. Median calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar)
    total number of transactions received by recipient from the contributor's zip code streamed in so far
    total amount of contributions received by recipient from the contributor's zip code streamed in so far


For the medianvals_by_zip code, I had many ideas but finally I used the simplest one that was extracting information of each line
and write the line to the txt. I get the result but I belive I could use numpy arrays to store the information of each line and finally 
save that in a txt file. This approach could be a faster approach. 

I made the input txt file smaller because I was not able to push the large itcont.txt file even with lfs on github.

Thank you so much for giving me this chance to compete in writing the code. I hope I am qualified for the next step to attend the 
classes and learn more about the data science.


Best regards.
Sepideh Dadashi


