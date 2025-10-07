@echo off
echo Stopping servers...

taskkill /FI "WindowTitle eq Python Server"
taskkill /FI "WindowTitle eq Go Server"

echo Servers stopped.
pause