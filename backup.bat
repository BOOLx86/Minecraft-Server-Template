set id=%random%

: Backup for world files
xcopy /s /e /i world "backup\%date:~6,4%_%date:~3,2%_%date:~0,2%-%id%\world"

: Backup for server jar
copy server.jar "backup\%date:~6,4%_%date:~3,2%_%date:~0,2%-%id%\server.jar"
