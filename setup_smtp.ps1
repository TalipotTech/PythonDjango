# ============================================
# SMTP Configuration for Email Integration
# ============================================
# This script sets up environment variables for Gmail SMTP
# 
# BEFORE RUNNING THIS:
# 1. Go to your Gmail account
# 2. Enable 2-Factor Authentication
# 3. Generate an App Password:
#    - Go to https://myaccount.google.com/apppasswords
#    - Select "Mail" and "Windows Computer"
#    - Copy the 16-character password (remove spaces)
# 4. Replace the values below with your details
#
# ============================================

# YOUR GMAIL SETTINGS (EDIT THESE)
$YOUR_EMAIL = "your-email@gmail.com"        # Your Gmail address
$YOUR_APP_PASSWORD = "your-16-char-app-password"  # Gmail App Password (no spaces)

# Set environment variables for current session
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "ensateadoor22@gmail.com"
$env:SMTP_PASSWORD = "uzfkmbjygspdgork"
$env:SMTP_USE_TLS = "True"
$env:SMTP_USE_SSL = "False"
$env:SENDER_EMAIL = "ensateadoor22@gmail.com"

Write-Host "✅ SMTP Configuration Set!" -ForegroundColor Green
Write-Host ""
Write-Host "Environment Variables:" -ForegroundColor Cyan
Write-Host "  SMTP_HOST: $env:SMTP_HOST"
Write-Host "  SMTP_PORT: $env:SMTP_PORT"
Write-Host "  SMTP_USER: $env:SMTP_USER"
Write-Host "  SMTP_PASSWORD: ****" # Hidden for security
Write-Host "  SENDER_EMAIL: $env:SENDER_EMAIL"
Write-Host ""
Write-Host "⚠️ NOTE: These variables are set for THIS PowerShell session only." -ForegroundColor Yellow
Write-Host "   They will be lost when you close this window." -ForegroundColor Yellow
Write-Host ""
Write-Host "To make them permanent (for your user account), run:" -ForegroundColor Cyan
Write-Host '  [System.Environment]::SetEnvironmentVariable("SMTP_HOST", "smtp.gmail.com", "User")' -ForegroundColor Gray
Write-Host '  [System.Environment]::SetEnvironmentVariable("SMTP_PORT", "587", "User")' -ForegroundColor Gray
Write-Host '  [System.Environment]::SetEnvironmentVariable("SMTP_USER", "your-email@gmail.com", "User")' -ForegroundColor Gray
Write-Host '  [System.Environment]::SetEnvironmentVariable("SMTP_PASSWORD", "your-app-password", "User")' -ForegroundColor Gray
Write-Host '  [System.Environment]::SetEnvironmentVariable("SMTP_USE_TLS", "True", "User")' -ForegroundColor Gray
Write-Host '  [System.Environment]::SetEnvironmentVariable("SENDER_EMAIL", "your-email@gmail.com", "User")' -ForegroundColor Gray
Write-Host ""
Write-Host "Now run your Django server in THIS SAME PowerShell window!" -ForegroundColor Green
