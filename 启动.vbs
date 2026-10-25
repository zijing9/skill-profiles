' SKILL本地管理 · 无窗口启动器
Option Explicit

Dim fso, sh, base, homeDir, py, dshDir, f, logFile, errMsg

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")

base = fso.GetParentFolderName(WScript.ScriptFullName)
homeDir = sh.ExpandEnvironmentStrings("%USERPROFILE%")
py = ""

' 1) DSH 内置的 pythonw（无控制台）
dshDir = homeDir & "\.dsh\dsh-runtimes"
If fso.FolderExists(dshDir) Then
    For Each f In fso.GetFolder(dshDir).SubFolders
        If fso.FileExists(f.Path & "\dependencies\python\pythonw.exe") Then
            py = f.Path & "\dependencies\python\pythonw.exe"
        End If
    Next
End If

' 2) 系统 pythonw（跳过 WindowsApps 别名）
If py = "" Then
    On Error Resume Next
    py = sh.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\pythonw.exe"
    If Not fso.FileExists(py) Then py = "pythonw.exe"
    On Error GoTo 0
End If

sh.CurrentDirectory = base

On Error Resume Next
sh.Run """" & py & """ """ & base & "\app.py""", 0, False

If Err.Number <> 0 Then
    errMsg = "启动失败：" & Err.Description & vbCrLf & "解释器：" & py
    logFile = base & "\logs\startup-error.txt"
    Dim ts
    Set ts = fso.CreateTextFile(logFile, True)
    ts.WriteLine Now & " " & errMsg
    ts.Close
    MsgBox errMsg, 16, "SKILL本地管理"
End If
On Error GoTo 0
