# HurLLM

This is a Python library for accessing and using the proprietary closed-source, general-purpose Artificial Intelligence model named HurLLM that uses the Transformers architecture focused on conversational solutions.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install HurLLM.

```bash
pip install hurllm
```

```python
# code for installing all necessary dependencies
# import the main class
from hurllm import DependenciesInstaller
# instantiation of the main class object
dependencies_installer = DependenciesInstaller()
# run dependencies install method
dependencies_installer.install()
# displays the dependencies that were successfully installed and those that failed
dependencies_installer.describe()
# use the method below only if you want to uninstall all dependencies
# dependencies_installer.uninstall()

```

## Usage

```python
# code example for a conversation in chat mode
# import the main class
from hurllm import HurLLM

# instantiation of the main class object
hurllm = HurLLM(
    API_KEY='YOUR_API_KEY', # code of your api key
    response_index=0, # default answer index, the LLM returns three possible answers with indices from 0 to 2, index 0 will be the most likely answer
    language='en', # abbreviation of the default language that will be used in the questions and answers
    session_control=False # session control: if True, it enables the memorizing of previous conversations, if False, it only considers the current conversation
)

# add a file for analysis
# the "addFile" method accepts any file type and can be invoked two or more times consecutively to add multiple files
hurllm.addFile(path='image.jpg') # in the "path" parameter you must define the path of the file

# prompt for LLM model
prompt = 'Hello! Create a short, single paragraph story about this image.'
# send the prompt and capture the return response
answer = hurllm.conversation(
    prompt=prompt, # question/ask of user
    code_interpreter=False # code interpreter: if True, automatically run any Python code in the response, if False, just display the codes
)

# display the returned response
print(answer)

# capture other possible answer alternatives for the same question
other_answers = hurllm.getResponses()
# displays the other two possible responses, the default response returned by the "conversation" function will be the one defined in the "response_index" parameter
print('\n\nOTHER POSSIBLE ANSWERS:')
print('[SECOND ANSWER]: '+other_answers[1]) # display the second most likely answer
print('[THIRD ANSWER]: '+other_answers[2]) # display the third most likely answer

# release the object from memory
del hurllm # this will be required to end the session if you have enabled the "session_control" parameter, otherwise this line will be optional

```

## Contributing

We do not accept contributions that may result in changing the original code.

Please make sure to update tests as appropriate.

## License

This is proprietary software and its alteration and/or distribution without the developer's authorization is not permitted.
