# ============================================
# PERMANENT SMTP Configuration Setup
# ============================================
# This script sets up PERMANENT environment variables for Gmail SMTP
# that will persist across system restarts.
#
# BEFORE RUNNING THIS:
# 1. Ensure you have your Gmail App Password ready
#    (Get it from: https://myaccount.google.com/apppasswords)
# 2. Make sure 2-Factor Authentication is enabled on your Gmail
# 3. Run this script in PowerShell (NOT as Administrator)
#
# ============================================

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "  PERMANENT SMTP CONFIGURATION SETUP" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check if script is running with admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Host "⚠️  WARNING: Running as Administrator" -ForegroundColor Yellow
    Write-Host "   This will set SYSTEM-WIDE variables instead of USER variables." -ForegroundColor Yellow
    Write-Host "   It's better to run this as a regular user." -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (yes/no)"
    if ($continue -ne "yes") {
        Write-Host "❌ Setup cancelled." -ForegroundColor Red
        exit
    }
    $scope = "Machine"
} else {
    $scope = "User"
}

Write-Host "📧 Gmail SMTP Configuration" -ForegroundColor Green
Write-Host ""
Write-Host "This will set PERMANENT environment variables for your user account."
Write-Host "They will survive system restarts and terminal closures."
Write-Host ""

# Get Gmail credentials
Write-Host "Enter your Gmail credentials:" -ForegroundColor Cyan
Write-Host "(These will be stored as environment variables)" -ForegroundColor Gray
Write-Host ""

$email = Read-Host "Gmail address (e.g., ensateadoor22@gmail.com)"
$appPassword = Read-Host "Gmail App Password (16 characters, no spaces)" -AsSecureString

# Convert secure string to plain text
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($appPassword)
$appPasswordPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Validate inputs
if ([string]::IsNullOrWhiteSpace($email)) {
    Write-Host "❌ Error: Email address cannot be empty!" -ForegroundColor Red
    exit
}

if ([string]::IsNullOrWhiteSpace($appPasswordPlain)) {
    Write-Host "❌ Error: App Password cannot be empty!" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Setting environment variables..." -ForegroundColor Yellow
Write-Host ""

try {
    # Set permanent environment variables
    [System.Environment]::SetEnvironmentVariable("SMTP_HOST", "smtp.gmail.com", $scope)
    [System.Environment]::SetEnvironmentVariable("SMTP_PORT", "587", $scope)
    [System.Environment]::SetEnvironmentVariable("SMTP_USER", $email, $scope)
    [System.Environment]::SetEnvironmentVariable("SMTP_PASSWORD", $appPasswordPlain, $scope)
    [System.Environment]::SetEnvironmentVariable("SMTP_USE_TLS", "True", $scope)
    [System.Environment]::SetEnvironmentVariable("SENDER_EMAIL", $email, $scope)
    
    # Also set for current session
    $env:SMTP_HOST = "smtp.gmail.com"
    $env:SMTP_PORT = "587"
    $env:SMTP_USER = $email
    $env:SMTP_PASSWORD = $appPasswordPlain
    $env:SMTP_USE_TLS = "True"
    $env:SENDER_EMAIL = $email
    
    Write-Host "✅ SUCCESS! Environment variables set permanently!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Configuration Details:" -ForegroundColor Cyan
    Write-Host "  SMTP_HOST: smtp.gmail.com"
    Write-Host "  SMTP_PORT: 587"
    Write-Host "  SMTP_USER: $email"
    Write-Host "  SMTP_PASSWORD: ******* (hidden)"
    Write-Host "  SENDER_EMAIL: $email"
    Write-Host "  SMTP_USE_TLS: True"
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host "  NEXT STEPS" -ForegroundColor Yellow
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host ""
    Write-Host "1. Close ALL PowerShell/Terminal windows" -ForegroundColor White
    Write-Host "2. Close VS Code completely" -ForegroundColor White
    Write-Host "3. Reopen VS Code" -ForegroundColor White
    Write-Host "4. Open a new terminal" -ForegroundColor White
    Write-Host "5. Test with: python test_email_config.py" -ForegroundColor White
    Write-Host "6. Run Django: python manage.py runserver" -ForegroundColor White
    Write-Host ""
    Write-Host "⚡ These settings will now work EVERY TIME you restart!" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "❌ ERROR: Failed to set environment variables!" -ForegroundColor Red
    Write-Host "Error details: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible solutions:" -ForegroundColor Yellow
    Write-Host "  1. Try running this script again"
    Write-Host "  2. Check your PowerShell permissions"
    Write-Host "  3. Try running as Administrator (though not recommended)"
    exit 1
}

# Optional: Verify the variables are set
Write-Host "Verifying environment variables..." -ForegroundColor Cyan
Write-Host ""

$variables = @("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "SENDER_EMAIL", "SMTP_USE_TLS")
$allSet = $true

foreach ($var in $variables) {
    $value = [System.Environment]::GetEnvironmentVariable($var, $scope)
    if ($value) {
        if ($var -eq "SMTP_PASSWORD") {
            Write-Host "  ✅ $var is set (hidden)" -ForegroundColor Green
        } else {
            Write-Host "  ✅ $var = $value" -ForegroundColor Green
        }
    } else {
        Write-Host "  ❌ $var is NOT set" -ForegroundColor Red
        $allSet = $false
    }
}

Write-Host ""
if ($allSet) {
    Write-Host "✅ All environment variables verified successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some variables might not be set correctly." -ForegroundColor Yellow
    Write-Host "   Try closing and reopening your terminal." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
