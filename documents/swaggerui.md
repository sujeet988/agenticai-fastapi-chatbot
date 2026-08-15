## swagger ans some other ui
Purpose	URL
Chat API	http://127.0.0.1:9999/chat
Swagger UI	http://127.0.0.1:9999/docs
ReDoc	http://127.0.0.1:9999/redoc
OpenAPI JSON	http://127.0.0.1:9999/openapi.json

## Streamlit  run 
-streamlit run frontend.py
-streamlit run ui/streamlit_app.py
## for deactive venv
deactivate

-Then remove the broken venv:
 Remove-Item -Recurse -Force .\venv

 Create a fresh one:
 python -m venv venv
 .\venv\Scripts\Activate.ps1

 # verify python
 python --version
where.exe python

# install requirments.txt
python -m pip install -r requirements.txt

## local run by uvicorn only
python -m uvicorn api.main:app --reload


