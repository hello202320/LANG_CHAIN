
## LANG CHAIN
The application utilizes a Large Language Model (LLM) to generate responses specifically related to your PDF. The LLM is designed to refrain from answering questions that are not relevant to the document.
## Installation

Clone this repository and install the requirements:

```
pip install -r requirements.txt
```
or
```
pip3 install -r requirements.txt
```

Create a .env file and add your OpenAI API; here are some references:

```
https://js.langchain.com/docs/getting-started/guide-llm
```
```
https://platform.openai.com/account/api-keys
```

## Usage

```
streamlit run app.py
```
