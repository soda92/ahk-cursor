#Requires AutoHotKey v2.0
#SingleInstance Force

TraySetIcon "{resources}\mouse.ico"

global targetExe := ""
global ini := A_ScriptDir "\Cursor.ini"

; 读取上次保存的目标进程名
if FileExist(ini)
    targetExe := IniRead(ini, "config", "executable", targetExe)

; 解析命令行参数：-e xxx / --executable=xxx
for i, arg in A_Args {
    if (arg = "-e" || arg = "--executable") {
        if (i+1 <= A_Args.Length)
            targetExe := A_Args[i+1]
    } else if RegExMatch(arg, "^-e=(.+)$", &m) {
        targetExe := m[1]
    } else if RegExMatch(arg, "^--executable=(.+)$", &m) {
        targetExe := m[1]
    }
}

; 托盘菜单
A_TrayMenu.Delete()
A_TrayMenu.Add("Force jiggle", (*) => Jiggle())
A_TrayMenu.Add("Set target executable...", SetTarget)
A_TrayMenu.Add("Edit script", EditSelf)
A_TrayMenu.Add()
A_TrayMenu.Add("Exit", (*) => ExitApp())

; 定时检测 + 随机抖动
SetTimer(Watch, 200)
return

Watch() {
    global targetExe
    if (targetExe = "" || ProcessExist(targetExe)) {
        if (Random(1, 10) = 1) { ; 10% tick 概率抖动，避免过于频繁
            Jiggle()
        }
    }
}

Jiggle() {
    dx := Random(-2, 2)
    dy := Random(-2, 2)
    if (dx = 0 && dy = 0)
        dx := 1
    MouseMove dx, dy, 0, "R"
    Sleep 20
    MouseMove -dx, -dy, 0, "R"
}

SetTarget(*) {
    global targetExe, ini
    ib := InputBox(
        "Enter target executable name (e.g. game.exe). Leave blank to always jiggle.",
        "Set Executable", "w320 h150", targetExe
    )
    if (ib.Result = "OK") {
        targetExe := Trim(ib.Value)
        try IniWrite(targetExe, ini, "config", "executable")
    }
}

EditSelf(*) {
    Run("c:\Program Files\Notepad++\notepad++.exe " A_ScriptFullPath)
}
