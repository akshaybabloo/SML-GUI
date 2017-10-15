@ECHO OFF

IF EXIST %USERPROFILE%\Anaconda3\NUL (
    echo Anaconda 3 available. Activating root environment.
    activate root
    echo Running SML GUI.
    python -c "from smlgui.main import main; main()"
) ELSE (
    echo Anaconda 3 not available. Software might break.
    python -c "from smlgui.main import main; main()"
)