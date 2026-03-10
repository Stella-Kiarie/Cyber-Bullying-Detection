Param(
    [string]$Branch = "Dapash",
    [string]$Message = "Update files",
    [switch]$All
)

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repo

Write-Host "Repository root: $repo"

Write-Host "Fetching origin..."
git fetch origin

# Check for local branch
& git rev-parse --verify $Branch 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Switching to existing local branch '$Branch'..."
    git checkout $Branch
} else {
    # Check for remote branch
    $remoteCheck = & git ls-remote --heads origin $Branch
    if ($remoteCheck) {
        Write-Host "Creating local branch '$Branch' from origin/$Branch..."
        git checkout -b $Branch origin/$Branch
    } else {
        Write-Host "Creating new local branch '$Branch'..."
        git checkout -b $Branch
    }
}

# Stage changes (default: all)
if ($All.IsPresent) {
    Write-Host "Staging all changes..."
    git add .
} else {
    Write-Host "Staging all changes (default)..."
    git add .
}

# Check if anything is staged
$staged = (& git diff --cached --name-only) -join "`n"
if (-not [string]::IsNullOrWhiteSpace($staged)) {
    Write-Host "Staged files:`n$staged"
    Write-Host "Committing with message: $Message"
    git commit -m "$Message"
    Write-Host "Pushing to origin/$Branch..."
    git push -u origin $Branch
} else {
    Write-Host "No staged changes to commit. Pushing branch reference to origin (if needed)..."
    git push -u origin $Branch
}

Write-Host "Done."
