Нужна детекция (край классификация) по снимкам с UAV/дронов скорость типа 10-15 FPS
Видео будет идти в 60 - 120 fps в зависимости от камеры, настраивается


Возможно надо будет привлекать диапазон частот спутника, ну или обойтись сообщениями с симки, api что то вроде телеграмм бота который скидывает корды пожара( или аппарата) и фотку


Датасеты на kaggle/в интернете, трекинг планируется фильтром калмана/deepsort
* https://www.kaggle.com/datasets/chandranaveenkumar/forest-fires-classification
Классификация


* Forest Fire | Kaggle 
Аэрофотки лесного пожара


* The wildfire dataset | Kaggle 
Большой датасет (не строго аэро-) фоточек


* UAV Thermal Imaginary - Fire Dataset | Kaggle
        Вероятно, кривущий (юзабилити 2,5) датасет ИК-фоток лесных пожаров. По идее должен быть сильно полезнее в плане поиска возгораний, но дым не видно.


* GitHub - DeepQuestAI/Fire-Smoke-Dataset: dataset for training fire and frame detection AI


* Data article Aerial imagery pile burn detection using DL: The FLAME dataset 
The FLAME dataset | IEEE DataPort - ссылка на данные


FiredetectionintheJungle Image Dataset (128)
forest-fire Image Dataset (181)
Fire Images Image Dataset (2003)
Flame 3 Diffusion (2083) (added)
ForestFireDetection (302)
Forest_smoke_collect Computer Vision Project (5054)


Модели для бенча 
Smoke & Fire F1 score=.99.9% | Kaggle
GitHub - OlafenwaMoses/FireNET | [arXiv 1905.11922] FireNet: IoT Model 






Стоимость выхода в production
Если jetson orin большой - то 500к только на плату, если нано 70к.
если вывезем на Orange Pi5 Pro, что сделала neural magic, то 20к и модули на симку и тп, плюс независимость от nvidia, сейчас проблемы с поставками jetson сами знаете почему


Платформа
Для тестов (читай прикинуть стоимость) - можно искать аренду
Пример “большой”  платформы - Геоскан 701
Более простая база - Геоскан 201. Нашел даже пост, как его применяют с очень похожей целью. 
Оба могут нести на себе тепловизор / обычную камеру.


Дальнейшая реализация подразумевает полную автоматизацию операций с БПЛА, как DJI Dock или Zipline. Текущие решения требуют серьезного обслуживания на земле и не подходят полноценно под задачи постоянного мониторинга.


Имеется вопрос с расположением компьюта:
*  на БПЛА - самый оперативный вариант, моментальный пинг о детекте по радиоканалу в случае чего.
* даунлинк в реалтайме - нужно поресерчить технические ограничения
* выгрузка и обработка между вылетами - медленно, может требовать повторного вылета для подтверждения, что еще сильнее замедляет работу.
Данные можно фидить большим моделям типа GroundingDino/Detic/Че найдем и получать почти размеченные датасеты
Стэк:
* torch/torchvision
* roboflow/CVAT
* OpenCV/CV2/skimage/че удобно
* ultralytics
* autodistill


Литература:
1. Wiki


2. Forest Fire Identification in UAV Imagery Using X-MobileNet
3. Early Forest Fire Detection Using Drones and Artificial Intelligence


4. Forest fire flame and smoke detection from UAV-captured images using fire-specific color features and multi-color space local binary pattern
        Хорошая статья


5. https://doi.org/10.1109/ICIAI.2019.8850815 
портативное решение с YOLOv3, 6.5 FPS / 83% детект


6. https://www.sciencedirect.com/science/article/pii/S2949855423000345?via%3Dihub - Свежачок, август 2023


7. Comets - проект по созданию системы мониторинга от Еврокомиссии (2003 год)


8. Forest Fire Monitoring System Based on UAV Team, Remote Sensing, and Image Processing  - разработка очень похожей системы


Распределение задач
Тимур - обзор существующих решений, обоснование задачи
Свят/Миша - поиск датасетов
Георгий - архитектура проекта
Миша - работа над оформлением в продукт и презентацией