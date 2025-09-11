forked from here https://github.com/farahrefaai/langchain-course


we are using uv as package manager

install uv using the command in their document

pip3 install uv

initiate a uv template

uv init

this will create the lock files and the env

using uv, add langchain and langchain-ollama (in the course its langchain-openai)

uv add langchain
uv add langchain-ollama


then add python-dotenv

uv add python-dotenv


and add black and isort for having a good looking code

uv add black isort


since ollama is a local open source model, we need to install the model locally from their website
after downloading ollama, you need to download a model, I chose llama3 done by meta
