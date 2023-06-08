@echo off

rem Define the list of dependencies
set "dependencies=wikipedia arxiv langchain kivy speech_recognition"

rem Iterate over each dependency
for %%d in (%dependencies%) do (
    rem Check if the dependency is installed
    python -c "import %%d" >nul 2>&1

    rem If the dependency is not installed, install it
    if errorlevel 1 (
        echo Installing %%d...
        pip install %%d
    ) else (
        echo %%d is already installed.
    )
)

echo All dependencies are installed.


python GPT4ALL_Android_OpenAI_langchain.py