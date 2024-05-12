import subprocess 
import os
import json
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = open("API_KEY","r").read()

def run_cpp_program():
    run_command = ["./cpp_program"]
    run_process = subprocess.run(run_command,  stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    if(run_process.returncode == 0):
            print("cpp program run succeeded, Output: " + run_process.stdout.decode()) 
            return run_process.returncode, run_process.stdout.decode()
    else:
             if run_process.stderr:
                print("cpp program run failed, Error: " + run_process.stderr.decode()) 
             else:
                print("cpp program run failed at runtime with no error message.")
    return  run_process.returncode, run_process.stderr.decode()

def compile_cpp_program():
    compile_command = ["g++", "cpp_program.cpp", "-o", "cpp_program"] 
    print("Compiling cpp program...")
    compile_process = subprocess.run(compile_command,   stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

    return compile_process.returncode
 
def compile_and_run_cpp_program():
    compile_command = ["g++", "cpp_program.cpp", "-o", "cpp_program"]  
    run_command     = ["./cpp_program"] 
    compile_process = subprocess.run(compile_command,   stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

    print("Compiling cpp program...") 
 
    if compile_process.returncode == 0: 
        print("Compilation successful.") 
        run_process = subprocess.run(run_command,  stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        print("returncode :" + str(run_process.returncode))
        
        if(run_process.returncode == 0):
            print("cpp program run succeeded, Output: " + run_process.stdout.decode()) 
            return compile_process.returncode, run_process.stdout.decode()
        else:
             if run_process.stderr:
                print("cpp program run failed, Error: " + run_process.stderr.decode()) 
             else:
                print("cpp program run failed at runtime with no error message.")
        return compile_process.returncode, run_process.stderr.decode()  

    else: 
        print("Compilation failed.") 
        print(compile_process.stderr.decode()) 
    return compile_process.returncode

def generate_Chatgpt_Prompt(code,description):
  background  = "I'm getting runtime error in my c++ program, could you identify and fix the problem for me? In your response do not give me any comments \
    Your solution can not contain any empty lines"

  description = "This is the description of the program" + description
  
  current_solution = "This is my current solution that does not work " + code + " \
   In your response do not remove any class or method. I want you to correct the class called Solution so that it works"

  includes         = "Do not include any libraries in your response, assume that they are already there"
  return str(background) + str(description) +  str(current_solution) +  str(includes) 

def send_Chatgpt_Request(prompt):
  print("Sending query to chatGPT...\n")
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

def append(filename,content_to_append):
    with open(filename, 'a') as file:
            file.writelines(content_to_append)
    
def overwrite_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error: Failed to overwrite the file '{file_path}': {e}")
        return False
    
def read_problems_json(problemIndx):
    with open('leetcode_problems.json', 'r') as file:
        json_data = json.load(file)

    outputs        = json_data["problems"][problemIndx]["outputs"]
    struct         = json_data["problems"][problemIndx]["struct"]
    code           = json_data["problems"][problemIndx]["code"]
    mainFunction   = json_data["problems"][problemIndx]["mainFunction"]
    printFunction  = json_data["problems"][problemIndx]["printFunction"]
    description    = json_data["problems"][problemIndx]["description"]
    return code,outputs,struct,mainFunction,printFunction,description

def write_results_to_file(actual,expected):
    file = open('results.txt', 'a')
    lines = ["Result: {}".format(actual),"Expected: {}".format(expected),"=============================="]

    for line in lines:
        file.write(line)
        file.write("\n")

    file.close()            

def compose_program(struct,code,printFunction,mainFunction):
     append("cpp_program.cpp",struct)
     append("cpp_program.cpp",code)            # the code Solution remains the same over all function calls 
     append("cpp_program.cpp",printFunction)   # print function remains the same over all function calls (needed for checking results std.out)
     append("cpp_program.cpp",mainFunction)    # test function

def attempt_all_test_cases_with_chatgpt_response(struct,chatgptResponse,testCases,printFunction,mainFunction,outputs):
    i = 0
    print("Attempting all test cases with chatgpt solution...\n")
    while i < testCases:
        reset_cpp_program("cpp_program.cpp")
        compose_program(struct,chatgptResponse,printFunction,mainFunction[i]) # between test cases everything should stay the same except the main function with the different function call
        if(compile_cpp_program() == 0):                                       #for each test case compile the program generated by chatGPT, we only give chatGPT one attempt,otherwise we would loop
            print("Compilation successful, executing program...")
            returncode,result = run_cpp_program()
            write_results_to_file(result, outputs[i])
        else:
            print("ChatGPT program compilation fail")
            break
        i += 1

def main():
    code,outputs,struct,mainFunction,printFunction,description = read_problems_json(21)      # read problem [i] from json (0-21)
    overwrite_file("results.txt","")

    for i in range(len(mainFunction)):             # for each test case compose,compile and run - if we get runtime error we start querying chatgpt                   
        print("Attempting test case: " + str(i)) 
        reset_cpp_program("cpp_program.cpp")
        compose_program(struct,code,printFunction,mainFunction[i])          
        if(compile_cpp_program() == 0):             # program managed to compile, now check for runtime error                 
            print("Compilation successful, executing program...")
            returncode,result = run_cpp_program()
            if(returncode != 0):       # program did not execute succesfully, now we need to ask chatgpt for if it can fix it, ask for code and then use code for all test cases!
                prompt   = generate_Chatgpt_Prompt(code,description)         
                response = send_Chatgpt_Request(prompt)
                attempt_all_test_cases_with_chatgpt_response(struct,response,len(mainFunction),printFunction,mainFunction,outputs)
                break # we invoked a runtime exception and asked chatgpt for help, we tried all test cases with the solution now we are done with this problem break out of this problem
            else:
                print("Original program did not have runtime error")
        else:
            print("Original program compilation fail") 
            break
     
 
                                                           
  

main()
