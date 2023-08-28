# GPT Engine

GPT Engine is a Python module that allows you to interact with the OpenAI API to generate text. It can be used for a variety of tasks, such as generating creative text formats, like poems, code, scripts, musical pieces, email, letters, etc., or answering your questions in an informative way.

To use GPT Engine, you will need to create a free account with OpenAI and get an API key. You can then install the GPT Engine module using pip:

pip install gptEngine
Once you have installed the module, you can create a GPT Engine object:

engine = GPTEngine(main_task="Generate Text", input_prompt="Write a poem about love.")
The main_task parameter specifies the type of task that you want to perform, and the input_prompt parameter specifies the input text that you want to provide to OpenAI.

To generate text, you can call the generate_response() method:

response = engine.generate_response("test.docx")
The generate_response() method takes the path to a .doc file as input. The text content of the file will be processed by OpenAI and a response will be generated.

The response from OpenAI will be returned as a string. You can then use the response as needed.
