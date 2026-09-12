$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
& "$PSScriptRoot\.venv\Scripts\python.exe" -m streamlit run app.py --server.port 8511 --server.address 127.0.0.1 --server.headless true
