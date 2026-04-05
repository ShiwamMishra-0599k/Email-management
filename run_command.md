(to run: cntrl+shift+v)

# Run command:
- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# create env:
- py -3.10 -m venv .venv

# Activate .venv:
- .venv/scripts/activate.ps1

# Run chroma:
-  chroma run --path ./chroma_store

# Uvicorn:
- uvicorn main:app --reload
