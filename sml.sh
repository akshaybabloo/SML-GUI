#!/bin/sh
if [-d "~/anaconda3"]; then
    echo "Anaconda 3 available. Activating root environment."
    source activate root
    echo "Running SML GUI."
    python -c "from smlgui.main import main; main()"
    else
    echo "Anaconda 3 not available. Software might break."
    python -c "from smlgui.main import main; main()"
fi