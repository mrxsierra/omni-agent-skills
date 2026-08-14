# Cross-Platform PowerShell Installer for omni-agent-skills (Windows / macOS / Linux PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "🚀 Installing omni-agent-skills (v0.0.1) across desktop platforms..." -ForegroundColor Cyan

# Determine User Home Directory
$UserHome = [System.Environment]::GetFolderPath("UserProfile")
$TargetDir = Join-Path $UserHome ".omni-agent-skills"

# Create Target Directories
$SkillsDir = Join-Path $TargetDir "skills"
$RulesDir = Join-Path $TargetDir "rules"

New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null
New-Item -ItemType Directory -Force -Path $RulesDir | Out-Null

# Copy Skills and Rules
$RepoRoot = $PSScriptRoot
if (-not $RepoRoot) { $RepoRoot = Get-Location }

Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\*") $SkillsDir
Copy-Item -Recurse -Force (Join-Path $RepoRoot "rules\*") $RulesDir
Copy-Item -Force (Join-Path $RepoRoot "registry.json") $TargetDir
Copy-Item -Force (Join-Path $RepoRoot "llms.txt") $TargetDir

Write-Host "✅ Cross-platform installation complete!" -ForegroundColor Green
Write-Host "📍 Installed to: $TargetDir" -ForegroundColor Yellow
