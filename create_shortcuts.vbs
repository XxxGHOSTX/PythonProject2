' ═══════════════════════════════════════════════════════════════════════════════
'  THALOS PRIME - Shortcut Creator
'  Creates desktop shortcuts for all Thalos interfaces
' ═══════════════════════════════════════════════════════════════════════════════

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get paths
strScriptPath = fso.GetParentFolderName(WScript.ScriptFullName)
strDesktop = WshShell.SpecialFolders("Desktop")

' Create Thalos Prime folder on desktop
strThalosFolder = strDesktop & "\Thalos Prime"
If Not fso.FolderExists(strThalosFolder) Then
    fso.CreateFolder(strThalosFolder)
End If

' ═══════════════════════════════════════════════════════════════════════════════
' SHORTCUT 1: Coding Agent (Main)
' ═══════════════════════════════════════════════════════════════════════════════
Set oShortcut = WshShell.CreateShortcut(strThalosFolder & "\⚡ Coding Agent.lnk")
oShortcut.TargetPath = strScriptPath & "\launch_coding_agent.bat"
oShortcut.WorkingDirectory = strScriptPath
oShortcut.Description = "Thalos Prime Coding Agent - Superior SBI Code Generation"
oShortcut.IconLocation = "shell32.dll,176"
oShortcut.Save

' ═══════════════════════════════════════════════════════════════════════════════
' SHORTCUT 2: Deploy Server (All Interfaces)
' ═══════════════════════════════════════════════════════════════════════════════
Set oShortcut = WshShell.CreateShortcut(strThalosFolder & "\🚀 Deploy Server.lnk")
oShortcut.TargetPath = strScriptPath & "\deploy_auto.bat"
oShortcut.WorkingDirectory = strScriptPath
oShortcut.Description = "Thalos Prime - Launch Deployment Server"
oShortcut.IconLocation = "shell32.dll,13"
oShortcut.Save

' ═══════════════════════════════════════════════════════════════════════════════
' SHORTCUT 3: SBI App
' ═══════════════════════════════════════════════════════════════════════════════
Set oShortcut = WshShell.CreateShortcut(strThalosFolder & "\🧠 SBI App.lnk")
oShortcut.TargetPath = strScriptPath & "\run_thalos.bat"
oShortcut.Arguments = "sbi"
oShortcut.WorkingDirectory = strScriptPath
oShortcut.Description = "Thalos Prime SBI Application"
oShortcut.IconLocation = "shell32.dll,44"
oShortcut.Save

' ═══════════════════════════════════════════════════════════════════════════════
' SHORTCUT 4: Prime App
' ═══════════════════════════════════════════════════════════════════════════════
Set oShortcut = WshShell.CreateShortcut(strThalosFolder & "\💻 Prime App.lnk")
oShortcut.TargetPath = strScriptPath & "\run_thalos.bat"
oShortcut.Arguments = "prime"
oShortcut.WorkingDirectory = strScriptPath
oShortcut.Description = "Thalos Prime Application"
oShortcut.IconLocation = "shell32.dll,15"
oShortcut.Save

' ═══════════════════════════════════════════════════════════════════════════════
' SHORTCUT 5: Setup Environment
' ═══════════════════════════════════════════════════════════════════════════════
Set oShortcut = WshShell.CreateShortcut(strThalosFolder & "\🔧 Setup Environment.lnk")
oShortcut.TargetPath = strScriptPath & "\setup_env.bat"
oShortcut.WorkingDirectory = strScriptPath
oShortcut.Description = "Setup Thalos Prime Environment"
oShortcut.IconLocation = "shell32.dll,21"
oShortcut.Save

' ═══════════════════════════════════════════════════════════════════════════════
' Create main shortcut on desktop root
' ═══════════════════════════════════════════════════════════════════════════════
Set oShortcut = WshShell.CreateShortcut(strDesktop & "\Thalos Prime Coding Agent.lnk")
oShortcut.TargetPath = strScriptPath & "\launch_coding_agent.bat"
oShortcut.WorkingDirectory = strScriptPath
oShortcut.Description = "Thalos Prime Coding Agent - Superior SBI Code Generation"
oShortcut.IconLocation = "shell32.dll,176"
oShortcut.Save

WScript.Echo "═══════════════════════════════════════════════════════════════" & vbCrLf & _
             "           THALOS PRIME SHORTCUTS CREATED!" & vbCrLf & _
             "═══════════════════════════════════════════════════════════════" & vbCrLf & vbCrLf & _
             "Shortcuts created:" & vbCrLf & _
             "  ✓ Desktop: Thalos Prime Coding Agent" & vbCrLf & _
             "  ✓ Desktop\Thalos Prime\⚡ Coding Agent" & vbCrLf & _
             "  ✓ Desktop\Thalos Prime\🚀 Deploy Server" & vbCrLf & _
             "  ✓ Desktop\Thalos Prime\🧠 SBI App" & vbCrLf & _
             "  ✓ Desktop\Thalos Prime\💻 Prime App" & vbCrLf & _
             "  ✓ Desktop\Thalos Prime\🔧 Setup Environment" & vbCrLf & vbCrLf & _
             "Click OK to close."

Set oShortcut = Nothing
Set WshShell = Nothing
Set fso = Nothing
