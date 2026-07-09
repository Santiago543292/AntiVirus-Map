Param(
    [string]$Repo = ".",
    [string]$Target = "AntiVirus0.1.0.exe",
    [string]$Pattern = "AntiVirus0.1.0.exe.part*",
    [string]$Archive = ""
)

Set-Location -Path $Repo
$parts = Get-ChildItem -Filter $Pattern | Sort-Object Name
if (-not $parts) {
    Write-Error "No parts matching '$Pattern' found in $Repo"
    exit 2
}

$out = Join-Path $Repo $Target
if (Test-Path $out) {
    Write-Host "$out already exists; skipping assembly."
} else {
    try {
        $fs = [System.IO.File]::OpenWrite($out)
        foreach ($p in $parts) {
            $bytes = [System.IO.File]::ReadAllBytes($p.FullName)
            $fs.Write($bytes, 0, $bytes.Length)
        }
        $fs.Close()
        Write-Host "Assembled $out from $($parts.Count) part(s)."
    } catch {
        if (Test-Path $out) { Remove-Item $out -ErrorAction SilentlyContinue }
        Write-Error "Assembly failed: $_"
        exit 1
    }
}

if ($Archive) {
    $archivePath = Join-Path $Repo $Archive
    if (Test-Path $archivePath) {
        Write-Host "$archivePath already exists; skipping archive creation."
    } else {
        try {
            Compress-Archive -Path $out -DestinationPath $archivePath -Force
            Write-Host "Created $archivePath from $out."
        } catch {
            Write-Error "Archive creation failed: $_"
            exit 1
        }
    }
}

exit 0
