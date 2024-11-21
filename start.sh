#!/bin/sh
while true
do
python3 main.py
echo "Если вы хотите полностью остановить процесс сейчас, нажмите Ctrl+C до истечения времени!"
echo "Перезагрузка через:"
for i in 5 4 3 2 1
do
echo "$i..."
sleep 1
done
echo "Перезагрузка!"
done 
