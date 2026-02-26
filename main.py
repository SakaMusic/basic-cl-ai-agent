import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


MAX_ITERATIONS = 20

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("api key has not been found in .env")
    
    # Get user prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Store user prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    # Instantiate AI agent
    client = genai.Client(api_key=api_key)

    for _ in range(MAX_ITERATIONS):
        function_results = []
            
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt,
                                            #    temperature=0,
                                            tools=[available_functions]
                                            )
        )
        
        # adding previous AI response back to message list
        if response.candidates:
            for interaction in response.candidates:
                messages.append(interaction.content)

        if response.usage_metadata is not None:
            if args.verbose == True:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            raise RuntimeError("Failed API request, no response metadata")
        

        if response.function_calls:
            for fc in response.function_calls:
                function_call_result = call_function(fc, verbose=args.verbose)
            
                if len(function_call_result.parts) == 0:
                    raise Exception("Error: empty parts list")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("Error: Expected FunctionResponse object, received None")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Error: Expected function result, recieved None")
                
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            if function_results:   
                messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            return
    
    print("ERROR: Max iterations reached with no final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()
