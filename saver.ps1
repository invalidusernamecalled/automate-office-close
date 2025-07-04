$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"
$outputFile = "session_list_$timestamp.txt"
$lines = @()

# Word docs
try {
    $word = [Runtime.InteropServices.Marshal]::GetActiveObject("Word.Application")
    foreach ($doc in $word.Documents) {
        $lines += $doc.FullName
    }
} catch {}

# Excel files
try {
    $excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
    foreach ($wb in $excel.Workbooks) {
        $lines += $wb.FullName
    }
} catch {}

# Explorer folders
try {
    $shell = New-Object -ComObject "Shell.Application"
    foreach ($window in $shell.Windows()) {
        if ($window.FullName -like "*explorer.exe") {
            $lines += $window.Document.Folder.Self.Path
        }
    }
} catch {}

$lines | Set-Content -Encoding ASCII $outputFile
(Get-Item $outputFile).Attributes = 'Hidden'

try {
    $word = [Runtime.InteropServices.Marshal]::GetActiveObject("Word.Application")
    foreach ($doc in $word.Documents) {
        if (-not $doc.Saved) {
            $doc.Save()
        }
    }
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
} catch {
    Write-Host "Word not running."
}

try {
    $excel = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
foreach ($wb in $excel.Workbooks) {
    if (-not $wb.Saved) {
        $wb.Save()
    }
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
}

} catch {
    # Excel wasn't running — start it
    Write-Host "Excel not running"
}

# Proceed with save and quit

foreach ($window in $shell.Windows()) {
    if ($window.FullName -like "*explorer.exe") {
        $window.Quit()
    }
}


