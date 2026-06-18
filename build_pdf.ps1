$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PaperDir = Join-Path $Root "paper"
$DownloadsPdf = Join-Path $env:USERPROFILE "Downloads\59.pdf"
$LocalPdf = Join-Path $PaperDir "main.pdf"
$BuildStatus = Join-Path $Root "data\build_status.json"
$ValidationPath = Join-Path $Root "results\full_scale\experiment_validation.json"

if (-not (Test-Path -LiteralPath $ValidationPath)) {
    throw "Missing full-scale validation file: $ValidationPath"
}

$Validation = Get-Content -Raw -LiteralPath $ValidationPath | ConvertFrom-Json
if (-not $Validation.row_count_ok) {
    throw "Full-scale validation row_count_ok is false."
}
if (-not $Validation.full_scale_ok) {
    throw "Full-scale validation full_scale_ok is false."
}
if ([int64]$Validation.condition_rows -ne 430080) {
    throw "Unexpected condition row count: $($Validation.condition_rows)"
}
if ([int64]$Validation.represented_evaluations -ne 112742891520) {
    throw "Unexpected represented evaluation count: $($Validation.represented_evaluations)"
}
if ([int64]$Validation.represented_planning_tick_decisions -ne 7215545057280) {
    throw "Unexpected represented planning tick count: $($Validation.represented_planning_tick_decisions)"
}
if ($Validation.best_non_oracle_policy -ne "adaptive_switch_gate") {
    throw "Unexpected best non-oracle policy: $($Validation.best_non_oracle_policy)"
}

Push-Location $PaperDir
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    bibtex main | Out-Null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
    pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-Null
}
finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $LocalPdf)) {
    throw "Expected local PDF was not produced: $LocalPdf"
}

$PdfInfo = & pdfinfo $LocalPdf
$PagesLine = $PdfInfo | Select-String -Pattern "^Pages:\s+(\d+)" | Select-Object -First 1
if (-not $PagesLine) {
    throw "Could not read page count from $LocalPdf"
}
$Pages = [int]$PagesLine.Matches[0].Groups[1].Value
if ($Pages -lt 25) {
    throw "Final PDF has $Pages pages; expected at least 25 pages."
}

$LocalLength = (Get-Item -LiteralPath $LocalPdf).Length
$Hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $LocalPdf).Hash

Copy-Item -LiteralPath $LocalPdf -Destination $DownloadsPdf -Force
Remove-Item -LiteralPath $LocalPdf -Force

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $BuildStatus) | Out-Null
$Status = [ordered]@{
    paper = 59
    decision = "final_v3_full_scale_submission_candidate"
    canonical_pdf = $DownloadsPdf
    pages = $Pages
    file_size_bytes = $LocalLength
    sha256 = $Hash
    condition_rows = [int64]$Validation.condition_rows
    represented_evaluations = [int64]$Validation.represented_evaluations
    represented_planning_tick_decisions = [int64]$Validation.represented_planning_tick_decisions
    best_non_oracle_policy = [string]$Validation.best_non_oracle_policy
    best_non_oracle_utility = [double]$Validation.best_non_oracle_utility
    oracle_utility = [double]$Validation.oracle_utility
    fixed_switch_success = [double]$Validation.fixed_switch_success
    adaptive_switch_success = [double]$Validation.adaptive_switch_success
    full_scale_ok = [bool]$Validation.full_scale_ok
    local_pdf_removed = -not (Test-Path -LiteralPath $LocalPdf)
    built_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")
}
$Status | ConvertTo-Json | Set-Content -Path $BuildStatus -Encoding ASCII

Get-Item -LiteralPath $DownloadsPdf | Select-Object FullName,Length,LastWriteTime
Write-Host "pages=$Pages"
Write-Host "sha256=$Hash"
Write-Host "local_pdf_removed=$(-not (Test-Path -LiteralPath $LocalPdf))"
