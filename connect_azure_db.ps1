# Quick script to connect to Azure PostgreSQL using psql
# Make sure you have PostgreSQL client tools installed

$env:PGPASSWORD = "Talipot@123"

Write-Host "Connecting to Azure PostgreSQL..." -ForegroundColor Green
Write-Host "Server: ensatepgserver.postgres.database.azure.com" -ForegroundColor Cyan
Write-Host ""

# Connect to Azure PostgreSQL
psql "host=ensatepgserver.postgres.database.azure.com port=5432 dbname=postgres user=pgAdmin sslmode=require"
