# Installation Script for JWT API and Hit Counter
# Run this script to install all required packages and set up the API

Write-Host "=" -ForegroundColor Cyan
Write-Host "🚀 Ensate Workshops - API Installation" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install required packages
Write-Host "📦 Step 1: Installing required packages..." -ForegroundColor Yellow
pip install djangorestframework==3.14.0
pip install djangorestframework-simplejwt==5.3.0
pip install django-cors-headers==4.3.0
pip install django-filter==23.5

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Packages installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Error installing packages" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Create migrations
Write-Host "📝 Step 2: Creating database migrations..." -ForegroundColor Yellow
python manage.py makemigrations

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Migrations created successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Error creating migrations" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 3: Run migrations
Write-Host "💾 Step 3: Applying migrations to database..." -ForegroundColor Yellow
python manage.py migrate

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Migrations applied successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Error applying migrations" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=" -ForegroundColor Green
Write-Host "✅ Installation Complete!" -ForegroundColor Green
Write-Host "=" -ForegroundColor Green
Write-Host ""

Write-Host "📚 API Documentation:" -ForegroundColor Cyan
Write-Host "   API Overview:     http://127.0.0.1:8000/api/" -ForegroundColor White
Write-Host "   Register User:    POST http://127.0.0.1:8000/api/auth/register/" -ForegroundColor White
Write-Host "   Login (JWT):      POST http://127.0.0.1:8000/api/auth/token/" -ForegroundColor White
Write-Host "   Refresh Token:    POST http://127.0.0.1:8000/api/auth/token/refresh/" -ForegroundColor White
Write-Host "   Sessions:         GET http://127.0.0.1:8000/api/sessions/" -ForegroundColor White
Write-Host "   Attendees:        GET http://127.0.0.1:8000/api/attendees/" -ForegroundColor White
Write-Host ""

Write-Host "🔐 Authentication:" -ForegroundColor Cyan
Write-Host "   1. Register: POST to /api/auth/register/" -ForegroundColor White
Write-Host "   2. Login: POST to /api/auth/token/ with username & password" -ForegroundColor White
Write-Host "   3. Use token: Add 'Authorization: Bearer <access_token>' header" -ForegroundColor White
Write-Host ""

Write-Host "🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Run: python manage.py runserver" -ForegroundColor White
Write-Host "   2. Visit: http://127.0.0.1:8000/api/" -ForegroundColor White
Write-Host "   3. Test API endpoints using Postman or curl" -ForegroundColor White
Write-Host ""

Write-Host "📊 Hit Counter:" -ForegroundColor Cyan
Write-Host "   Automatically tracking all page visits" -ForegroundColor White
Write-Host "   View stats: http://127.0.0.1:8000/api/stats/dashboard/" -ForegroundColor White
Write-Host ""
