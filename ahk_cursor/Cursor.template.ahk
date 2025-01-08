#Requires AutoHotKey v2.0
#SingleInstance Force

TraySetIcon "{resources}\mouse.ico"

id := 0
id2 := 0

Run "ahk-cursor-stop-cli.exe", , "Hide", &id2
ProcessWaitClose(id2)
Run "ahk-cursor-cli.exe", , "Hide", &id

MyFunc(ExitReason, ExitCode) {
    Run "ahk-cursor-stop-cli.exe", , "Hide", &id2
    ProcessWaitClose(id2)
}

Persistent
OnExit MyFunc
