[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [string]$TexExe = "I:\Tools\texlive\2026\bin\windows\xelatex.exe",

    [string]$OutDir = "",

    [switch]$Png,

    [string]$PngExe = "I:\Tools\texlive\2026\bin\windows\pdftocairo.exe",

    [int]$PngDpi = 160,

    [int]$PngWidth = 0,

    [int]$PngHeight = 0,

    [string]$PngStem = ""
)

$ErrorActionPreference = "Stop"

$sourcePath = (Resolve-Path -LiteralPath $Source).Path

if (-not (Test-Path -LiteralPath $TexExe)) {
    $command = Get-Command xelatex.exe -ErrorAction SilentlyContinue
    if ($null -eq $command) {
        throw "xelatex.exe was not found. Pass -TexExe with a valid TeX Live path."
    }
    $TexExe = $command.Source
}

if ([string]::IsNullOrWhiteSpace($OutDir)) {
    $outDirPath = Split-Path -Parent $sourcePath
} else {
    if (-not (Test-Path -LiteralPath $OutDir)) {
        New-Item -ItemType Directory -Path $OutDir | Out-Null
    }
    $outDirPath = (Resolve-Path -LiteralPath $OutDir).Path
}

$texInput = $sourcePath -replace "\\", "/"
$texOutDir = $outDirPath -replace "\\", "/"

& $TexExe -interaction=nonstopmode -halt-on-error "-output-directory=$texOutDir" $texInput
if ($LASTEXITCODE -ne 0) {
    throw "XeLaTeX failed with exit code $LASTEXITCODE."
}

$pdfPath = Join-Path $outDirPath ([IO.Path]::GetFileNameWithoutExtension($sourcePath) + ".pdf")
if (-not (Test-Path -LiteralPath $pdfPath)) {
    throw "Expected PDF was not created: $pdfPath"
}

Write-Output "PDF written: $pdfPath"

if ($Png) {
    if (-not (Test-Path -LiteralPath $PngExe)) {
        $pngCommand = Get-Command pdftocairo.exe -ErrorAction SilentlyContinue
        if ($null -eq $pngCommand) {
            throw "pdftocairo.exe was not found. Pass -PngExe with a valid TeX Live path."
        }
        $PngExe = $pngCommand.Source
    }

    if ([string]::IsNullOrWhiteSpace($PngStem)) {
        $pngStemPath = Join-Path $outDirPath ([IO.Path]::GetFileNameWithoutExtension($sourcePath))
    } else {
        $pngStemPath = $PngStem
        if (-not [IO.Path]::IsPathRooted($pngStemPath)) {
            $pngStemPath = Join-Path (Get-Location).Path $pngStemPath
        }
        if ([IO.Path]::GetExtension($pngStemPath).ToLowerInvariant() -eq ".png") {
            $pngStemPath = Join-Path ([IO.Path]::GetDirectoryName($pngStemPath)) ([IO.Path]::GetFileNameWithoutExtension($pngStemPath))
        }
    }

    $pngDir = [IO.Path]::GetDirectoryName($pngStemPath)
    if (-not [string]::IsNullOrWhiteSpace($pngDir) -and -not (Test-Path -LiteralPath $pngDir)) {
        New-Item -ItemType Directory -Path $pngDir | Out-Null
    }

    if ($PngWidth -gt 0 -and $PngHeight -gt 0) {
        & $PngExe -png -singlefile -scale-to-x $PngWidth -scale-to-y $PngHeight $pdfPath $pngStemPath
    } elseif ($PngWidth -gt 0) {
        & $PngExe -png -singlefile -scale-to-x $PngWidth $pdfPath $pngStemPath
    } elseif ($PngHeight -gt 0) {
        & $PngExe -png -singlefile -scale-to-y $PngHeight $pdfPath $pngStemPath
    } else {
        & $PngExe -png -singlefile -r $PngDpi $pdfPath $pngStemPath
    }

    if ($LASTEXITCODE -ne 0) {
        throw "PNG export failed with exit code $LASTEXITCODE."
    }

    $pngPath = "$pngStemPath.png"
    if (-not (Test-Path -LiteralPath $pngPath)) {
        throw "Expected PNG was not created: $pngPath"
    }

    Write-Output "PNG written: $pngPath"
}
