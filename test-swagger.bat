@echo off
echo Testando Swagger dos Microsservicos...
echo.

echo 1. Iniciando containers...
docker-compose up -d --build

echo.
echo 2. Aguardando containers iniciarem...
timeout /t 30

echo.
echo 3. Testando URLs do Swagger:
echo.

echo API Gateway: http://localhost:8000/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:8000/apidocs/ || echo "ERRO: API Gateway nao responde"

echo MS-Usuarios: http://localhost:5001/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5001/apidocs/ || echo "ERRO: MS-Usuarios nao responde"

echo MS-Espacos: http://localhost:5002/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5002/apidocs/ || echo "ERRO: MS-Espacos nao responde"

echo MS-Reservas: http://localhost:5003/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5003/apidocs/ || echo "ERRO: MS-Reservas nao responde"

echo MS-Pagamentos: http://localhost:5004/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5004/apidocs/ || echo "ERRO: MS-Pagamentos nao responde"

echo MS-Precos: http://localhost:5005/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5005/apidocs/ || echo "ERRO: MS-Precos nao responde"

echo MS-Checkin: http://localhost:5006/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5006/apidocs/ || echo "ERRO: MS-Checkin nao responde"

echo MS-Notificacoes: http://localhost:5007/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5007/apidocs/ || echo "ERRO: MS-Notificacoes nao responde"

echo MS-Financeiro: http://localhost:5008/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5008/apidocs/ || echo "ERRO: MS-Financeiro nao responde"

echo MS-Analytics: http://localhost:5009/apidocs/
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5009/apidocs/ || echo "ERRO: MS-Analytics nao responde"

echo.
echo 4. Verificando containers rodando:
docker-compose ps

echo.
echo 5. URLs para testar no browser:
echo - API Gateway Swagger: http://localhost:8000/apidocs/
echo - MS-Usuarios Swagger: http://localhost:5001/apidocs/
echo - MS-Espacos Swagger: http://localhost:5002/apidocs/
echo - MS-Reservas Swagger: http://localhost:5003/apidocs/
echo - MS-Pagamentos Swagger: http://localhost:5004/apidocs/
echo - MS-Precos Swagger: http://localhost:5005/apidocs/
echo - MS-Checkin Swagger: http://localhost:5006/apidocs/
echo - MS-Notificacoes Swagger: http://localhost:5007/apidocs/
echo - MS-Financeiro Swagger: http://localhost:5008/apidocs/
echo - MS-Analytics Swagger: http://localhost:5009/apidocs/
echo - Frontend: http://localhost:3000

pause