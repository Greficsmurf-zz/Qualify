# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import sys, traceback                       # Импортируем библиотеки для обработки исключений

from time import sleep                      # Импортируем библиотеку для работы со временем
from re import findall                      # Импортируем библиотеку по работе с регулярными выражениями
from subprocess import check_output 

try:
    tempOn = 60                             # Температура включения кулера
    controlPin = 14                         # Пин отвечающий за управление
    pinState = False                        # Актуальное состояние кулера
    
    # === Инициализация пинов ===
    GPIO.setmode(GPIO.BCM)                  # Режим нумерации в BCM
    GPIO.setup(controlPin, GPIO.OUT, initial=0) # Управляющий пин в режим OUTPUT

    while True:                             # Бесконечный цикл запроса температуры
                         # Получаем значение температуры
       if int(input("Please enter your age: ")) > 18:
            pinState = not pinState         # Меняем статус состояния
            GPIO.output(controlPin, pinState)
       else: 
	    pinState = False
	    GPIO.output(controlPin, pinState) # Задаем новый статус пину управления
						 # Выводим температуру в консоль
       sleep(1)                            # Пауза - 1 секунда

except KeyboardInterrupt:
    # ...
    print("Exit pressed Ctrl+C") 
finally:
    GPIO.cleanup() 
