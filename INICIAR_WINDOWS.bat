@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
  echo Python nao foi encontrado. Instale Python 3.11 ou superior.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Criando ambiente virtual...
  py -m venv .venv
)

echo Instalando ou atualizando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Nao foi possivel instalar as dependencias.
  pause
  exit /b 1
)

echo.
echo LinguaQuest disponivel em http://127.0.0.1:5000
echo Pressione Ctrl+C para encerrar.
".venv\Scripts\python.exe" run.py
endlocal
