# Azure Cloud Deployment Guide

Complete guide to deploy Django backend and React frontend separately on Azure.

## 🎯 Overview

- **Backend**: Django API hosted on Azure App Service (Linux)
- **Frontend**: React app hosted on Azure Static Web Apps
- **Database**: Azure PostgreSQL (Already configured)

---

## 📋 Prerequisites

1. Azure Account with active subscription
2. Azure CLI installed: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
3. Node.js and npm installed
4. Python 3.11+ installed
5. Git installed

---

## 🔐 Part 1: Prepare Django Backend for Deployment

### Step 1: Login to Azure CLI

```powershell
az login
```

### Step 2: Create Resource Group (if not exists)

```powershell
az group create --name ensate-app-rg --location eastus
```

### Step 3: Create Azure App Service Plan

```powershell
az appservice plan create `
  --name ensate-backend-plan `
  --resource-group ensate-app-rg `
  --sku B1 `
  --is-linux
```

### Step 4: Create Web App for Django

```powershell
az webapp create `
  --name ensate-django-backend `
  --resource-group ensate-app-rg `
  --plan ensate-backend-plan `
  --runtime "PYTHON:3.11"
```

### Step 5: Configure Django App Settings

```powershell
# Set environment variables
az webapp config appsettings set `
  --name ensate-django-backend `
  --resource-group ensate-app-rg `
  --settings `
    DATABASE_URL="postgresql://pgAdmin:Talipot%40123@ensatepgserver.postgres.database.azure.com:5432/postgres?sslmode=require" `
    SECRET_KEY="your-super-secret-key-here" `
    DEBUG="False" `
    ALLOWED_HOSTS="ensate-django-backend.azurewebsites.net" `
    CSRF_TRUSTED_ORIGINS="https://ensate-django-backend.azurewebsites.net"
```

### Step 6: Deploy Django Backend

```powershell
# From project root directory
cd G:\Sandra\PYTHONDJANGO\PythonDjango

# Deploy using local git
az webapp deployment source config-local-git `
  --name ensate-django-backend `
  --resource-group ensate-app-rg

# Get deployment URL
az webapp deployment list-publishing-credentials `
  --name ensate-django-backend `
  --resource-group ensate-app-rg `
  --query scmUri `
  --output tsv

# Add Azure remote and push
git remote add azure <deployment-url-from-above>
git push azure main
```

---

## ⚛️ Part 2: Deploy React Frontend to Azure Static Web Apps

### Step 1: Build React App

```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango\react-frontend

# Update API endpoint in src/services/api.js to point to Azure backend
# Change: http://127.0.0.1:8000 
# To: https://ensate-django-backend.azurewebsites.net

npm run build
```

### Step 2: Create Static Web App

```powershell
az staticwebapp create `
  --name ensate-react-frontend `
  --resource-group ensate-app-rg `
  --source https://github.com/TalipotTech/PythonDjango `
  --location eastus2 `
  --branch main `
  --app-location "/react-frontend" `
  --output-location "build" `
  --login-with-github
```

### Alternative: Manual Upload via VS Code Extension

1. Install "Azure Static Web Apps" extension in VS Code
2. Sign in to Azure
3. Right-click on `react-frontend/build` folder
4. Select "Deploy to Static Web App"
5. Follow the prompts

---

## 🔧 Part 3: Configure CORS and Environment Variables

### Update Django settings.py for CORS

The CORS settings need to include your Azure frontend URL:

```python
CORS_ALLOWED_ORIGINS = [
    "https://ensate-react-frontend.azurestaticapps.net",
    "http://localhost:3000",  # For local development
]
```

### Update React API Configuration

Edit `react-frontend/src/services/api.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://ensate-django-backend.azurewebsites.net';
```

---

## 📦 Part 4: Verify Deployment

### Backend Health Check

```powershell
curl https://ensate-django-backend.azurewebsites.net/api/health/
```

### Frontend Access

Open browser: https://ensate-react-frontend.azurestaticapps.net

---

## 🔄 Part 5: Continuous Deployment Setup

### Backend CI/CD with GitHub Actions

GitHub Actions workflow will be created automatically when using Azure deployment.

### Frontend CI/CD

Static Web Apps automatically sets up GitHub Actions workflow in `.github/workflows/`

---

## 📊 Monitoring and Logs

### View Backend Logs

```powershell
az webapp log tail `
  --name ensate-django-backend `
  --resource-group ensate-app-rg
```

### View Frontend Logs

```powershell
az staticwebapp show `
  --name ensate-react-frontend `
  --resource-group ensate-app-rg
```

---

## 💰 Cost Estimation

- **App Service Plan B1**: ~$13/month
- **Static Web Apps (Standard)**: Free tier available, Standard ~$9/month
- **PostgreSQL**: Already running (check Azure portal for cost)

**Total estimated**: ~$22-30/month

---

## 🔐 Security Best Practices

1. ✅ Use Azure Key Vault for secrets
2. ✅ Enable HTTPS only
3. ✅ Configure firewall rules
4. ✅ Use managed identities
5. ✅ Regular backups
6. ✅ Monitor security alerts

---

## 🚀 Quick Deploy Commands Summary

```powershell
# 1. Login to Azure
az login

# 2. Deploy Backend
cd G:\Sandra\PYTHONDJANGO\PythonDjango
git push azure main

# 3. Deploy Frontend
cd react-frontend
npm run build
az staticwebapp deploy --app-name ensate-react-frontend

# 4. Check status
az webapp browse --name ensate-django-backend --resource-group ensate-app-rg
```

---

## 📝 Post-Deployment Checklist

- [ ] Backend is accessible via URL
- [ ] Frontend is accessible via URL
- [ ] Database connection works
- [ ] CORS is configured correctly
- [ ] Environment variables are set
- [ ] Static files are served correctly
- [ ] API endpoints respond correctly
- [ ] Authentication works
- [ ] Email functionality works (if configured)
- [ ] Admin panel is accessible
- [ ] Logs are being captured

---

## 🆘 Troubleshooting

### Backend Issues

```powershell
# Check logs
az webapp log tail --name ensate-django-backend --resource-group ensate-app-rg

# Restart app
az webapp restart --name ensate-django-backend --resource-group ensate-app-rg

# SSH into container
az webapp ssh --name ensate-django-backend --resource-group ensate-app-rg
```

### Frontend Issues

```powershell
# Check build logs
az staticwebapp show --name ensate-react-frontend --resource-group ensate-app-rg

# Rebuild
npm run build
az staticwebapp deploy
```

---

## 🔗 Useful Links

- Azure Portal: https://portal.azure.com
- App Service Documentation: https://docs.microsoft.com/en-us/azure/app-service/
- Static Web Apps Documentation: https://docs.microsoft.com/en-us/azure/static-web-apps/
- PostgreSQL Documentation: https://docs.microsoft.com/en-us/azure/postgresql/

---

## 📞 Support

For issues, contact Azure Support or check:
- Azure Status: https://status.azure.com
- GitHub Repository: https://github.com/TalipotTech/PythonDjango
