@echo off
REM setup_structure.bat
REM Automatically creates the SCIRAG production folder structure (Windows)

echo 🚀 Setting up SCIRAG production structure...
echo.

REM Create main directories
echo 📁 Creating directories...
mkdir backend\app\agents 2>nul
mkdir backend\app\api\routes 2>nul
mkdir backend\app\models 2>nul
mkdir backend\app\services 2>nul
mkdir backend\app\tests 2>nul
mkdir backend\scripts 2>nul
mkdir docs 2>nul
mkdir frontend 2>nul
mkdir papers 2>nul

REM Create __init__.py files for Python packages
echo 📝 Creating __init__.py files...
type nul > backend\app\__init__.py
type nul > backend\app\agents\__init__.py
type nul > backend\app\api\__init__.py
type nul > backend\app\api\routes\__init__.py
type nul > backend\app\models\__init__.py
type nul > backend\app\services\__init__.py
type nul > backend\app\tests\__init__.py

echo.
echo ✅ Folder structure created!
echo.
echo 📂 Your structure is ready!
echo.
echo Next steps:
echo 1. Move POC files to their locations (see FILE_PLACEMENT_GUIDE.md)
echo 2. cd backend
echo 3. python -m venv venv
echo 4. venv\Scripts\activate
echo 5. pip install -r requirements.txt
echo.
echo Happy coding! 🎉
pause