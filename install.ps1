# Cross-Platform PowerShell Installer for omni-agent-skills (Windows / macOS / Linux PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "🚀 Installing omni-agent-skills (v0.0.2) across desktop platforms..." -ForegroundColor Cyan

# Determine User Home Directory
$UserHome = [System.Environment]::GetFolderPath("UserProfile")
$TargetDir = Join-Path $UserHome ".omni-agent-skills"

# Create Target Directories
$SkillsDir = Join-Path $TargetDir "skills"
$RulesDir = Join-Path $TargetDir "rules"
$PromptsDir = Join-Path $TargetDir "prompts"
$SubagentsDir = Join-Path $TargetDir "subagents"
$SnippetsDir = Join-Path $TargetDir "snippets"
$HooksDir = Join-Path $TargetDir "hooks"
$McpConfigsDir = Join-Path $TargetDir "mcp-configs"

New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null
New-Item -ItemType Directory -Force -Path $RulesDir | Out-Null
New-Item -ItemType Directory -Force -Path $PromptsDir | Out-Null
New-Item -ItemType Directory -Force -Path $SubagentsDir | Out-Null
New-Item -ItemType Directory -Force -Path $SnippetsDir | Out-Null
New-Item -ItemType Directory -Force -Path $HooksDir | Out-Null
New-Item -ItemType Directory -Force -Path $McpConfigsDir | Out-Null

# Copy Catalog Assets
$RepoRoot = $PSScriptRoot
if (-not $RepoRoot) { $RepoRoot = Get-Location }

Copy-Item -Recurse -Force (Join-Path $RepoRoot "registry\skills\*") $SkillsDir
Copy-Item -Recurse -Force (Join-Path $RepoRoot "registry\rules\*") $RulesDir
if (Test-Path (Join-Path $RepoRoot "registry\prompts")) { Copy-Item -Recurse -Force (Join-Path $RepoRoot "registry\prompts\*") $PromptsDir }
if (Test-Path (Join-Path $RepoRoot "registry\subagents")) { Copy-Item -Recurse -Force (Join-Path $RepoRoot "registry\subagents\*") $SubagentsDir }
if (Test-Path (Join-Path $RepoRoot "registry\snippets")) { Copy-Item -Recurse -Force (Join-Path $RepoRoot "registry\snippets\*") $SnippetsDir }
if (Test-Path (Join-Path $RepoRoot "registry\hooks")) { Copy-Item -Recurse -Force (Join-Path $RepoRoot "registry\hooks\*") $HooksDir }
if (Test-Path (Join-Path $RepoRoot "registry\mcp-configs")) { Copy-Item -Recurse -Force (Join-Path $RepoRoot "registry\mcp-configs\*") $McpConfigsDir }
Copy-Item -Force (Join-Path $RepoRoot "registry\registry.json") $TargetDir
Copy-Item -Force (Join-Path $RepoRoot "llms.txt") $TargetDir

Write-Host "✅ Cross-platform installation complete!" -ForegroundColor Green
Write-Host "📍 Installed to: $TargetDir" -ForegroundColor Yellow
