import subprocess 
import os
import shutil
import filecmp
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = open("API_KEY","r").read()

def compile_and_run_cpp_program():
    compile_command = ["g++", "cpp_program.cpp", "-o", "cpp_program"]  
    run_command     = ["./cpp_program"] 
    compile_process = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    print("Compiling cpp program...") 

    if compile_process.returncode == 0: 
        print("Compilation successful.") 
        run_process = subprocess.run(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        
        if(run_process.returncode == 0):
            print("cpp program run succeeded, Output: " + run_process.stdout.decode()) 
        else:
            print("cpp program run failed, Error: " + run_process.stderr.decode()) 
    else: 
        print("Compilation failed.") 
        print(compile_process.stderr.decode()) 

def read_Leetcode_Problem(): 
    with open("problemcodes.txt") as file_1, open("probleminputs.txt") as file_2, open("problemoutputs.txt") as file_3:
        problem = file_1.read()
        input   = file_2.read()
        output  = file_3.read()
    return problem,input,output

def generate_Chatgpt_Prompt(problem,input,output): 
  background       = "I'm getting runtime error in my c++ program, could you identify and fix the problem for me? The response should include "
  requirement      = "The solution should be able to call the function within the solution class with the following inputs : " + input + " and the corresponding outputs should be: " + output + "Also, I dont wan't any comments"
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
  return response.choices[0].message.content
    
def write_problem_to_cpp_program(filename,string_to_write):
    if not (filecmp.cmp('cpp_skeleton.cpp', 'cpp_program.cpp')): # Check if we need to reset the cpp_program (has run atleast once)
        shutil.copyfile('cpp_skeleton.cpp', 'cpp_program.cpp') 
        
    with open(filename, "r") as file:
        lines = file.readlines()

    start_index = -1
    end_index   = -1

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
 problem,input,output = read_Leetcode_Problem()                           # Store the problem and test case input/output
 prompt               = generate_Chatgpt_Prompt(problem,input,output)     # Generate the prompt for chatgpt 
 response             = send_Chatgpt_Request(prompt)                      # Send request to chatgpt and store response
 write_problem_to_cpp_program("cpp_program.cpp",response)                 # Insert the the response into cpp skeleton
 compile_and_run_cpp_program()                                            # Compile and run cpp program
  

main()
