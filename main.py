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

import subprocess 
import os
import shutil
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = open("API_KEY","r").read()

#API_KEY = open("API_KEY","r").read()
#openai.api_key = API_KEY
need_reset = False

def compile_and_run_cpp_program():
    compile_command = ["g++", "cpp_program.cpp", "-o", "cpp_program"] 
    
    run_command = ["./cpp_program"] 
    
    compile_process = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    print("Compiling cpp program...") 

    if compile_process.returncode == 0: 
        print("Compilation successful.") 
        run_process = subprocess.run(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        output = run_process.stdout.decode() 
       
        print("Return code: ", run_process.returncode)
        error  = run_process.stderr.decode() 
        
        print("Output:") 
        print(output) 
        
        print("Error:") 
        print(error) 
    else: 
        print("Compilation failed.") 
        print(compile_process.stderr.decode()) 


def read_Leetcode_Problem(): 
    with open("problemcodes.txt") as file_1, open("probleminputs.txt") as file_2, open("problemoutputs.txt") as file_3:
        problem = file_1.read()
        input   = file_2.read()
        output  = file_3.read()
        file_1.close()
        file_2.close()
        file_3.close()
    return problem,input,output


def generate_Chatgpt_Prompt(problem,input,output): 
  background = "I'm getting runtime error in my c++ program, could you identify and fix the problem for me? The response should include "
  requirement = "The solution should be able to call the function within the solution class with the following inputs : " + input + " and the corresponding outputs should be: " + output + "Also, I dont wan't any comments"
  current_solution = "This is my current solution that does not work " + problem + " The response should contain everything needed so that the solution can be compiled and run instantly" 
  return background + requirement + current_solution  




def send_Chatgpt_Request(prompt):  
  client = OpenAI()
  response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": prompt}
  ]
)
  with open("solution.txt","w") as file:
      file.write(response.choices[0].message.content)
  file.close()    


def write_problem_to_cpp_program(filename,string_to_write,need_reset):
    if (need_reset): # Check if we need to reset the cpp_program (has run atleast once)
        shutil.copyfile('cpp_skeleton.cpp', 'cpp_program.cpp') 
        
    with open(filename, "r") as file:
        lines = file.readlines()

    start_index = -1
    end_index = -1

    # Find the start and end index of the main function
    for i, line in enumerate(lines):
        if line.strip() == "int main() {":
            start_index = i + 1  # Start writing after the function declaration
        elif start_index != -1 and line.strip() == "}":
            end_index = i
            break

    if start_index == -1 or end_index == -1:
        print("Main function not found in", filename)
        return

    # Write the string to the file within the main function
    lines.insert(start_index, f'{string_to_write} \n')

    # Write the modified content back to the file
    with open(filename, "w") as file:
        file.writelines(lines)

def main():
 problem,input,output = read_Leetcode_Problem()
 write_problem_to_cpp_program("cpp_program.cpp",problem,False)
 #compile_and_run_cpp_program()
 prompt = generate_Chatgpt_Prompt(problem,input,output)
 send_Chatgpt_Request(prompt)  

main()
