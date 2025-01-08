#Requires AutoHotkey v2.0
id := 0

; not working
loop {
    if WinExist("ahk_exe BGI.exe") {
        if (id != 0) {
            Run "python.exe simple.py", , , &id
        }
    }
    else {
        ProcessClose(id)
        ProcessWaitClose(id)
        id := 0
    }

    Sleep 1000
}
