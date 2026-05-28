# GuestVision AI - Push to GitHub Script
# Run: .\push-to-github.ps1

Write-Host "🚀 GuestVision AI - GitHub Push Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Get GitHub URL from user
$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/guest-counter.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "❌ Repository URL cannot be empty" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Checking git status..." -ForegroundColor Yellow

# Check if git is installed
git --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git is not installed. Please install from https://git-scm.com/" -ForegroundColor Red
    exit 1
}

# Initialize git if needed
if (-not (Test-Path .git)) {
    Write-Host "🔧 Initializing git repository..." -ForegroundColor Yellow
    git init
    git config user.name "Your Name"
    git config user.email "your.email@example.com"
}

# Show what will be staged
Write-Host ""
Write-Host "📦 Files to be committed:" -ForegroundColor Yellow
git add .
git status --short | ForEach-Object { Write-Host "  $_" }

# Confirm before committing
Write-Host ""
$confirm = Read-Host "Continue with commit? (y/n)"
if ($confirm -ne "y") {
    Write-Host "❌ Cancelled" -ForegroundColor Red
    exit 1
}

# Create commit
Write-Host ""
Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: GuestVision AI - Full-stack IoT event management system"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Commit failed" -ForegroundColor Red
    exit 1
}

# Add remote
Write-Host ""
Write-Host "🔗 Adding remote repository..." -ForegroundColor Yellow
$existingRemote = git config --get remote.origin.url
if ([string]::IsNullOrWhiteSpace($existingRemote)) {
    git remote add origin $repoUrl
} else {
    Write-Host "ℹ️  Remote already exists: $existingRemote" -ForegroundColor Gray
}

# Push to GitHub
Write-Host ""
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Success! Project pushed to GitHub" -ForegroundColor Green
    Write-Host "📍 Repository: $repoUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Go to: $repoUrl" -ForegroundColor Cyan
    Write-Host "  2. Add collaborators in Settings → Collaborators" -ForegroundColor Cyan
    Write-Host "  3. Create GitHub Actions for CI/CD (optional)" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Check your credentials and try again." -ForegroundColor Red
    exit 1
}
