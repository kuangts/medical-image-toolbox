cd $PSScriptRoot
git pull

if ( -Not (Test-Path .venv -PathType Container) )
{
    python -m venv .venv
}
.\.venv\Scripts\Activate.ps1
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r .\requirements.txt
python main.py
deactivate
