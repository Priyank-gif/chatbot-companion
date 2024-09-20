
# Chatbot Companion

This project uses LangChain and Gemini Model/\
\


## Installation

#### Install Python
```
Version: 3.10.0
```

- Install on [Windows](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)

#### Setup virtual environment
```markdown
 python -m venv venv
```
#### activate virtual environment
```cmd
  .\venv\Scripts\activate  
```


#### Install project dependencies

```cmd
  pip install -r requirements.txt
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`GOOGLE_API_KEY`

#### Run project API's

```cmd
  uvicorn app.main:app --reload

```

