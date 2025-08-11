@echo off
echo ========================================
echo    ADVBS - INICIANDO APLICACAO
echo ========================================
echo.

echo [1/2] Iniciando Backend (Flask)...
start "Backend - Flask" cmd /k "cd advBS-backend\poker_academy_api && python src\main.py"

echo [2/2] Aguardando 3 segundos e iniciando Frontend (React)...
timeout /t 3 /nobreak > nul

start "Frontend - React" cmd /k "cd advBS && npm start"

echo.
echo ========================================
echo    APLICACAO INICIADA COM SUCESSO!
echo ========================================
echo.
echo Backend rodando em: http://localhost:5000
echo Frontend rodando em: http://localhost:3000
echo.
echo CREDENCIAIS DE TESTE:
echo.
echo ADMIN:
echo   Email: admin@advtransito.com
echo   Senha: admin123
echo.
echo CLIENTE:
echo   Email: cliente@teste.com
echo   Senha: cliente123
echo.
echo Pressione qualquer tecla para fechar...
pause > nul
