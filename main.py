#inputs can be "correct" or "wrong" 

#input can be "correct" = there exists an implementation of algorithm (based on the "textual specifications") that does not throw an exception, and possibly gives the correct output
#input can be "wrong" = there NOT exists an implementation of algorithm (based on the "textual specifications") that does not throw an exceptions, and at the same time provides correct output with "correct" inputs

#[*] function can be "erroneous" or "healed"
#Function can be "erroneous" = for inputs that are "correct", it may happen (depending on the input, always correct) that the code throws an exeception (crashes)
#def. "errorInputs" = "correct inputs that provoke execption in the erroneous function"
#Function can be "healed" = for inputs that are NOT "errorInputs", the output should be the same given by "erroneous" function (i.e., we want to preserve the functionality in case the input is not one that provokes exception). On the other hand, for inputs that ARE "errorInputs", the healed code should
#	- not throw an exeception
#	- possibly, provides an output that is in line with the "textual specifications" of the function
	
	
#For us, the healed code should provide the same output of the "erroneous-code"


def read_Leetcode_Problem(): # Ideally automize through leetcode api 
    fd = open("problemcodes.txt", "r")
    problem = fd.read()
    fd = open("probleminputs.txt", "r")
    input = fd.read() 
    fd = open("problemoutputs.txt", "r")
    output = fd.read()
    run_Test_Code(problem,input,output)


def generate_Chatgpt_Prompt(): # Example, chatgpt Give me the code without comments so i can easily save and run it
    print ("")




def send_Chatgpt_Request():  # Chatgpt api send prompt and fetch answer from chatgpt 
    print ("")


# We attempt one healing iteration of the code
# Does it still have runtime error? 
    # Yes - Healing failed
    # No - How accurate was the healed code? 3/4 test cases = 75% healed



def run_Test_Code(problem,input,output): #Ideally execute locally  - hard
    print (problem)
    print (input)
    print (output)
    # Create a skeleton cpp file with main function
    # Edit the skeleton with the "solution" from problemcodes.txt by inserting it in the wrapping main function
    # Run the cpp program with the input from probleminput.txt
    # Check for runtime error and if the output equals problemoutputs.txt value
    

    #Problem File 
    #Input File
    #Expected Output File
 


# Run the code function locally with the input and check with the expected output file 
        
# test case input [4,3,2] expected output [2,3,4] 



def main():
   read_Leetcode_Problem()

main()


# Create a dummy cpp template to encapsulate problems
# Save leetcode problem file as cpp file



# 1 Read leetcode problem from file - store 
# 2 Create prompt (Template) (Customize)?
# 3 Make chatgpt call with prompt, send and retrieve
# 3 Submit to leetcode                      -- Look for api leetcode submission, else manually submit and collect result
# 4 ChatGPT api call with prompt 