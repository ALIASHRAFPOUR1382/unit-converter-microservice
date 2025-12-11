# Auto-commit script for gradual project updates
# This script automatically commits changes

param(
    [string]$Message = "",
    [switch]$Push = $false,
    [int]$Interval = 0
)

# Function to check for changes
function Check-Changes {
    $status = git status --porcelain
    return $status -ne $null -and $status.Length -gt 0
}

# Function to generate commit message
function Get-CommitMessage {
    param([string]$CustomMessage)
    
    if ($CustomMessage -ne "") {
        return $CustomMessage
    }
    
    $status = git status --short
    $files = ($status | ForEach-Object { ($_ -split '\s+')[1] }) -join ', '
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    return "Auto-commit: Changes in $files - $timestamp"
}

# Function to commit changes
function Commit-Changes {
    param(
        [string]$Message,
        [bool]$ShouldPush = $false
    )
    
    Write-Host "Checking for changes..." -ForegroundColor Yellow
    
    if (-not (Check-Changes)) {
        Write-Host "No changes to commit." -ForegroundColor Green
        return $false
    }
    
    Write-Host "Changes found. Committing..." -ForegroundColor Yellow
    
    # Add all changes
    git add -A | Out-Null
    
    # Create commit
    $commitMessage = Get-CommitMessage -CustomMessage $Message
    $result = git commit -m $commitMessage 2>&1
    
    if ($LASTEXITCODE -eq 0 -or $?) {
        Write-Host "Commit successful: $commitMessage" -ForegroundColor Green
        
        if ($ShouldPush) {
            Write-Host "Pushing to remote..." -ForegroundColor Yellow
            $pushResult = git push 2>&1
            
            if ($LASTEXITCODE -eq 0 -or $?) {
                Write-Host "Push successful." -ForegroundColor Green
            } else {
                Write-Host "Push failed." -ForegroundColor Red
            }
        }
        
        return $true
    } else {
        Write-Host "Commit failed." -ForegroundColor Red
        return $false
    }
}

# Main execution
if ($Interval -gt 0) {
    Write-Host "Monitoring mode activated. Checking every $Interval seconds..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop." -ForegroundColor Yellow
    Write-Host ""
    
    while ($true) {
        Commit-Changes -Message $Message -ShouldPush $Push
        Start-Sleep -Seconds $Interval
    }
} else {
    Commit-Changes -Message $Message -ShouldPush $Push
}
