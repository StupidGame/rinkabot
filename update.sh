cd /home/bronzeasia/rinkabot
screen -S rinkabot -X quit
git pull
screen -S rinkabot -m -d
screen -S rinkabot -X stuff "python rinka.py\r"
