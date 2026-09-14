@echo off
chcp 65001 >nul
setlocal
set "SITE=%~dp0site\index.html"
if exist "%SITE%" goto open
echo 首次使用：正在生成中文版离线网站（约需数秒）...
where py >nul 2>nul
if %errorlevel%==0 (
  py "%~dp0site\build_site.py" --source-root "%~dp0..\.."
) else (
  python "%~dp0site\build_site.py" --source-root "%~dp0..\.."
)
:open
if not exist "%SITE%" (
  echo.
  echo 生成失败：请先安装 Python 3，或手动运行：
  echo   py "%~dp0site\build_site.py" --source-root "%~dp0..\.."
  pause
  exit /b 1
)
start "" "%SITE%"
