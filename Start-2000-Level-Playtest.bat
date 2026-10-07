@echo off
setlocal
set "PREVIEW=%~dp0design\campaign-2000-preview\index.html"
if not exist "%PREVIEW%" (
  echo Playtest preview not found: %PREVIEW%
  pause
  exit /b 1
)
start "" "%PREVIEW%"
endlocal
