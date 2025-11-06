# Azure Deployment Script for Ensate Application
# Run this script to deploy both frontend and backend to Azure

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Ensate Application - Azure Deployment" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$RESOURCE_GROUP = "ensate-app-rg"
$LOCATION = "eastus"
$BACKEND_APP_NAME = "ensate-django-backend"
$FRONTEND_APP_NAME = "ensate-react-frontend"
$APP_SERVICE_PLAN = "ensate-backend-plan"

# Check if Azure CLI is installed
Write-Host "Checking Azure CLI..." -ForegroundColor Yellow
$azureCliInstalled = Get-Command az -ErrorAction SilentlyContinue
if (-not $azureCliInstalled) {
    Write-Host "❌ Azure CLI is not installed. Please install it first." -ForegroundColor Red
    Write-Host "Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit
}
Write-Host "✅ Azure CLI is installed" -ForegroundColor Green

# Login to Azure
Write-Host ""
Write-Host "Step 1: Login to Azure" -ForegroundColor Yellow
az login

# Create Resource Group
Write-Host ""
Write-Host "Step 2: Creating Resource Group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION
Write-Host "✅ Resource Group created" -ForegroundColor Green

# Create App Service Plan
Write-Host ""
Write-Host "Step 3: Creating App Service Plan..." -ForegroundColor Yellow
az appservice plan create `
    --name $APP_SERVICE_PLAN `
    --resource-group $RESOURCE_GROUP `
    --sku B1 `
    --is-linux
Write-Host "✅ App Service Plan created" -ForegroundColor Green

# Create Web App for Django
Write-Host ""
Write-Host "Step 4: Creating Django Web App..." -ForegroundColor Yellow
az webapp create `
    --name $BACKEND_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --plan $APP_SERVICE_PLAN `
    --runtime "PYTHON:3.11"
Write-Host "✅ Django Web App created" -ForegroundColor Green

# Configure App Settings
Write-Host ""
Write-Host "Step 5: Configuring Django App Settings..." -ForegroundColor Yellow

$SECRET_KEY = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | ForEach-Object {[char]$_})

az webapp config appsettings set `
    --name $BACKEND_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --settings `
        DATABASE_URL="postgresql://pgAdmin:Talipot%40123@ensatepgserver.postgres.database.azure.com:5432/postgres?sslmode=require" `
        SECRET_KEY="$SECRET_KEY" `
        DEBUG="False" `
        ALLOWED_HOSTS="$BACKEND_APP_NAME.azurewebsites.net" `
        CSRF_TRUSTED_ORIGINS="https://$BACKEND_APP_NAME.azurewebsites.net" `
        DJANGO_SETTINGS_MODULE="questionnaire_project.settings_production" `
        WEBSITES_PORT="8000"

Write-Host "✅ App Settings configured" -ForegroundColor Green

# Configure Startup Command
Write-Host ""
Write-Host "Step 6: Configuring Startup Command..." -ForegroundColor Yellow
az webapp config set `
    --name $BACKEND_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --startup-file "startup.sh"
Write-Host "✅ Startup command configured" -ForegroundColor Green

# Deploy Django Backend
Write-Host ""
Write-Host "Step 7: Deploying Django Backend..." -ForegroundColor Yellow
Write-Host "Please wait, this may take a few minutes..." -ForegroundColor Cyan

# Configure local git deployment
$deployUrl = az webapp deployment source config-local-git `
    --name $BACKEND_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query url `
    --output tsv

Write-Host "Deployment URL: $deployUrl" -ForegroundColor Cyan

# Add Azure remote
cd $PSScriptRoot
git remote remove azure -ErrorAction SilentlyContinue
git remote add azure $deployUrl

# Push to Azure
Write-Host "Pushing code to Azure..." -ForegroundColor Yellow
git push azure main

Write-Host "✅ Django Backend deployed" -ForegroundColor Green

# Build React Frontend
Write-Host ""
Write-Host "Step 8: Building React Frontend..." -ForegroundColor Yellow
cd react-frontend

# Update environment variable
$envContent = "REACT_APP_API_URL=https://$BACKEND_APP_NAME.azurewebsites.net"
Set-Content -Path ".env.production" -Value $envContent

npm install
npm run build
Write-Host "✅ React Frontend built" -ForegroundColor Green

# Create Static Web App
Write-Host ""
Write-Host "Step 9: Creating Static Web App..." -ForegroundColor Yellow
Write-Host "⚠️  This will open browser for GitHub authentication..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

az staticwebapp create `
    --name $FRONTEND_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --source "https://github.com/TalipotTech/PythonDjango" `
    --location "eastus2" `
    --branch "main" `
    --app-location "/react-frontend" `
    --output-location "build" `
    --login-with-github

Write-Host "✅ Static Web App created" -ForegroundColor Green

# Update Backend CORS
Write-Host ""
Write-Host "Step 10: Updating CORS Settings..." -ForegroundColor Yellow
$frontendUrl = "https://$FRONTEND_APP_NAME.azurestaticapps.net"

az webapp config appsettings set `
    --name $BACKEND_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --settings `
        CORS_ALLOWED_ORIGINS="$frontendUrl,http://localhost:3000"

Write-Host "✅ CORS settings updated" -ForegroundColor Green

# Display URLs
Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend URL:  https://$BACKEND_APP_NAME.azurewebsites.net" -ForegroundColor Cyan
Write-Host "Frontend URL: https://$FRONTEND_APP_NAME.azurestaticapps.net" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Visit the frontend URL to test your application" -ForegroundColor White
Write-Host "2. Check logs: az webapp log tail --name $BACKEND_APP_NAME --resource-group $RESOURCE_GROUP" -ForegroundColor White
Write-Host "3. Configure custom domain (optional)" -ForegroundColor White
Write-Host ""
Write-Host "📚 For more information, see AZURE_DEPLOYMENT_GUIDE.md" -ForegroundColor Yellow

# Open URLs in browser
Write-Host ""
$openBrowser = Read-Host "Do you want to open the applications in browser? (Y/N)"
if ($openBrowser -eq "Y" -or $openBrowser -eq "y") {
    Start-Process "https://$BACKEND_APP_NAME.azurewebsites.net"
    Start-Process "https://$FRONTEND_APP_NAME.azurestaticapps.net"
}

Write-Host ""
Write-Host "✅ Deployment script completed!" -ForegroundColor Green
