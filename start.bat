echo Starting Servers

cd Python
cd PythonProject
start "Python Server" python main.py
cd ..
cd ..
echo %cd%
cd Go
start "Go Server" go run main.go
cd ..

echo Both servers started.
pause