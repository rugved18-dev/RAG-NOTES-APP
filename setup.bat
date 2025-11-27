@echo off
REM Chat with Your Notes - Setup Script for Windows

echo.
echo ==================================================
echo  Chat with Your Notes - Setup
echo ==================================================
echo.

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create uploads directory
if not exist uploads (
    mkdir uploads
    echo ✓ Created uploads directory
) else (
    echo ✓ Uploads directory exists
)

REM Create .env file
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo ✓ Created .env file
    )
) else (
    echo ✓ .env file exists
)

REM Success message
echo.
echo ==================================================
echo ✓ Setup Complete!
echo ==================================================
echo.
echo Next Steps:
echo 1. Edit .env and add your OpenAI API key
echo    OPENAI_API_KEY=sk-...your-key-here...
echo.
echo 2. Run the application:
echo    streamlit run app/app.py
echo.
echo 3. Open http://localhost:8501 in your browser
echo.
echo Get an API key: https://platform.openai.com/api-keys
echo.
echo ==================================================
echo.
pause
    