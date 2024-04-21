import subprocess 
import os
import json
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
    with open("problemcodes.txt") as file_1, open("probleminputs.txt") as file_2, open("problemoutputs.txt") as file_3, open("problemparameters.txt") as file_4, open("problemstructs.txt") as file_5:
        problem   = file_1.read()
        input     = file_2.read()
        output    = file_3.read()
        parameter = file_4.read()
        struct    = file_5.read()
    return problem,input,output,parameter,struct

def generate_Chatgpt_Prompt(code,inputs,outputs,params):
  background       = "I'm getting runtime error in my c++ program, could you identify and fix the problem for me? Your solution should remove the runtime error and be able to pass the test case as described:"
  requirements     = "In your response I want the following: Add a main function that calls the solution class with the following parameter(s)" , params , " where the inputs used are " , inputs , " and the output should be " , outputs , "Also I don't want any comments."
  current_solution = "This is my current solution that does not work " + code + " The response should contain everything needed so that the solution can be compiled and run instantly, only modify the solution class do not remove any code that exists before it" 
  includes         = "Do not include any libraries in your response, assume that they are already there"
  # show previous prompts that did not work 
  return str(background) + str(requirements) +  str(current_solution) +  str(includes)

def send_Chatgpt_Request(prompt):  
  client = OpenAI()
  response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": prompt}
  ]
)
  return response.choices[0].message.content

def reset_cpp_program(filename):
    with open("cpp_includes.txt", 'r') as source_file:
        content = source_file.read()
    
    with open(filename, 'w') as file:
        file.write(content)

    print(f"File {filename} has been overwritten.")

def append_to_first_empty_line(filename, content_to_append):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Find the first empty line
    line_number = None
    for i, line in enumerate(lines):
        if line.strip() == '':
            line_number = i
            break

    if line_number is not None:
        # Insert the content after the first empty line
        lines.insert(line_number, content_to_append + '\n')

        # Write the modified content back to the file
        with open(filename, 'w') as file:
            file.writelines(lines)
    else:
        print("No empty line found in the file.")

def read_problems_json():
    with open('leetcode_problems.json', 'r') as file:
        json_data = json.load(file)

    params  = json_data["problems"][0]["params"]
    inputs  = json_data["problems"][0]["inputs"]
    outputs = json_data["problems"][0]["outputs"]
    struct  = json_data["problems"][0]["struct"]
    code    = json_data["problems"][0]["code"]
    print("Inputs: " , inputs)  
    print("Outputs: " , outputs)  
    print("Params: " , params)    
    return code,inputs,outputs,params,struct
    
def main():
    code,inputs,outputs,params,struct = read_problems_json()                             
    prompt                            = generate_Chatgpt_Prompt(code,inputs,outputs,params)         # Generate the prompt for chatgpt 
    response                          = send_Chatgpt_Request(prompt)                                # Send request to chatgpt and store response
    reset_cpp_program("cpp_program.cpp")                                                            # Overwrite the cpp file with only libraries to avoid chatgpt from adding its own libraries
    append_to_first_empty_line("cpp_program.cpp",struct)                                            # Since chatgpt removes pre defined structs for some reason, we store them ourselves and write to cpp file
    append_to_first_empty_line("cpp_program.cpp",response)
    compile_and_run_cpp_program()                                                               
  

main()
