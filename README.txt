[ACSOS24 – under review] Validating Large Language Models for Self-Healing (Anonymised for double-blind review.)

Prototype implementation for the Statistics builder.


The project is structured in the following files: 

leetcode_problems.json - Contains all problems that have been gathered from leetcode user submissions containing runtime errors
for each problem the following exists:

    1. name         -> Name of the leetcode problem and its id
    2. outputs      -> The expected output for each test case
    3. description  -> The textual description of the function taken from leetcode
    4. mainfunction -> Function that is used for testing the function 
    5. struct       -> For problems that are dependent on underlying structs they are put here
    6. code         -> The current source code for the function that is currently not working

API_KEY - Contains the api key for openAI api to work.

cpp_includes.txt - A skeleton file which contains all neccessary #includes

cpp_program.cpp - The skeleton cpp file which is populated with information such as includes from cpp_includes.txt and 
source code from leetcode_problems.json to be able to compile and run it. 

results.txt - Displays the result of the latest attempt at self healing with provided output vs expected output

main.py - The executable which performs the following: 

1. Reads a problem from leetcode_problems.json file, the problem chosen is done at line 165 read_problems_json(<problem_index>)
2. The program then iterates over each test case that the problem contains, this is taken from the leetcode_problems.json file 
3. In each iteration the program sets up a clean cpp file and then fill it with the following content:
    3.1. The neccessary headers such as #include <iostream> taken from cpp_includes.txt
    3.2. The source code for the failed solution taken from leetcode_problems.json
    3.3  The main function with the function call for each test case, also taken from leetcode_problems.json
4. After the cpp file has been put together with these components the program tries to compile and run it
5. If a runtime error is invoked for any of the test cases we query chatGPT requesting a solution. The information sent to chatGPT is the following:
    5.1 The current source code.
    5.2 The program description - what the problem is supposed to be able to do, taken from leetcode_problems.json
    5.3 The error code received from the runtime exception
6. Once the program has received a solution from chatGPT it iterates over all test cases again and runs them tt see if the new source code 
from chatGPT is able to pass the test cases to determine the succesfulness of the code healing.
7. The results from the executed test cases are printed out to the file results.txt to which the success can be examined 
