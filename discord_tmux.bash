#!/bin/bash

tmux new-session -d -s real

## Create the windows on which each node or .launch file is going to run
tmux send-keys -t real 'tmux new-window -n NAME1 ' ENTER
tmux send-keys -t real 'tmux new-window -n NAME2 ' ENTER

## Send the command to each window from window 0
# NAME1
tmux send-keys -t real "tmux send-keys -t NAME1 'PYTHONPATH=$(pwd) python3 main/core/event_handler/discord/event_handler.py' ENTER" ENTER
# NAME2
tmux send-keys -t real "tmux send-keys -t NAME2 'celery -A main.core.event_handler.discord.tasks worker -B -l info -c 4 -P threads' ENTER" ENTER
# NAME0
tmux send-keys -t real "tmux send-keys -t NAME0 'redis-commander' ENTER"
## Start a new line on window 0
tmux send-keys -t real ENTER

## Attach to session
tmux send-keys -t real "tmux select-window -t NAME2" ENTER
tmux attach -t real
