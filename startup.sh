session="lights"
tmux start-server
tmux new-session -d -s $session -n flask
#tmux selectp -t 1
tmux send-keys "cd ~/Code/gardenlights; export FLASK_APP=app.py; flask run" C-m
tmux splitw -h -p 50
tmux send-keys "htop" C-m
