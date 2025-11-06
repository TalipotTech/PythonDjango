# Quick Azure Deployment Steps

## 🚀 Deploy in 3 Simple Steps

### Step 1: Prepare Your Code

```powershell
cd G:\Sandra\PYTHONDJANGO\PythonDjango
git add .
git commit -m "Prepare for Azure deployment"
git push origin main
```

### Step 2: Run Automated Deployment Script

```powershell
.\deploy-azure.ps1
```

This script will:
- ✅ Create Azure resources
- ✅ Deploy Django backend
- ✅ Build and deploy React frontend
- ✅ Configure all settings automatically

### Step 3: Verify Deployment

Visit your URLs:
- **Backend**: https://ensate-django-backend.azurewebsites.net
- **Frontend**: https://ensate-react-frontend.azurestaticapps.net

---

## 📋 Manual Deployment (Alternative)

If you prefer manual control, follow these steps:

### Backend Deployment

```powershell
# 1. Login to Azure
az login

# 2. Create resources
az group create --name ensate-app-rg --location eastus

az appservice plan create `
  --name ensate-backend-plan `
  --resource-group ensate-app-rg `
  --sku B1 `
  --is-linux

az webapp create `
  --name ensate-django-backend `
  --resource-group ensate-app-rg `
  --plan ensate-backend-plan `
  --runtime "PYTHON:3.11"

# 3. Configure settings
az webapp config appsettings set `
  --name ensate-django-backend `
  --resource-group ensate-app-rg `
  --settings @azure-settings.json

# 4. Deploy code
git remote add azure $(az webapp deployment source config-local-git --name ensate-django-backend --resource-group ensate-app-rg --query url --output tsv)
git push azure main
```

### Frontend Deployment

```powershell
# 1. Build React app
cd react-frontend
npm install
npm run build

# 2. Deploy to Static Web Apps
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

---

## 🔧 Post-Deployment Configuration

### 1. Update Django CORS

```powershell
az webapp config appsettings set `
  --name ensate-django-backend `
  --resource-group ensate-app-rg `
  --settings CORS_ALLOWED_ORIGINS="https://ensate-react-frontend.azurestaticapps.net"
```

### 2. Run Migrations

```powershell
az webapp ssh --name ensate-django-backend --resource-group ensate-app-rg
python manage.py migrate
python manage.py createsuperuser
exit
```

### 3. Collect Static Files

Static files are automatically collected during startup.

---

## 📊 Monitoring

### View Backend Logs

```powershell
az webapp log tail --name ensate-django-backend --resource-group ensate-app-rg
```

### View Application Status

```powershell
az webapp show --name ensate-django-backend --resource-group ensate-app-rg --query state
```

---

## 🔄 Update Deployment

### Update Backend

```powershell
git add .
git commit -m "Update backend"
git push azure main
```

### Update Frontend

Frontend updates automatically via GitHub Actions when you push to main branch.

---

## 🆘 Troubleshooting

### Backend Not Starting

```powershell
# Check logs
az webapp log tail --name ensate-django-backend --resource-group ensate-app-rg

# Restart app
az webapp restart --name ensate-django-backend --resource-group ensate-app-rg
```

### Frontend Not Loading

```powershell
# Check build status
az staticwebapp show --name ensate-react-frontend --resource-group ensate-app-rg

# Rebuild
cd react-frontend
npm run build
```

### Database Connection Issues

- Verify DATABASE_URL in app settings
- Check PostgreSQL firewall rules
- Ensure SSL is enabled

---

## 💰 Cost Management

### Check Current Costs

```powershell
az consumption usage list --query "[].{Service:instanceName, Cost:pretaxCost}" -o table
```

### Stop Resources to Save Costs

```powershell
# Stop backend (when not in use)
az webapp stop --name ensate-django-backend --resource-group ensate-app-rg

# Start backend
az webapp start --name ensate-django-backend --resource-group ensate-app-rg
```

---

## 🗑️ Cleanup (Delete Everything)

```powershell
az group delete --name ensate-app-rg --yes --no-wait
```

---

## 📞 Get Help

- Azure Portal: https://portal.azure.com
- Documentation: See AZURE_DEPLOYMENT_GUIDE.md
- GitHub Issues: https://github.com/TalipotTech/PythonDjango/issues
