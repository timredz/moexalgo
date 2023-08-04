# MOEX ISS/API wrapper
Это удобная в работе аналитика обертка над API MOEX/ISS предоставляющего доступ 
к данных размещенным на информационно-статистическом сервере Московской Биржи.

### Инсталляция пакета в виртуальное окружение разработчика
Проект надо инсталлировать в виртуальное окружение. Виртуальное окружение можно создать отдельно 
или в настройках проекта при открытии в PyCharm `File > Settings > Project > Python interpreter`.
Далее открыть Terminal в PyCharm или активировать виртуальное окружение в командной строке.
Выполнить следующие команды:
```shell
# инсталляция проекта
pip install -U pip setuptools wheel
pip install -e .
```

### Для тестирования в Jupyter Notebook
Инсталлируйте пакет в виртуальное окружение, как описано выше. Далее выполните следущие команды:
```shell
# Активация pandas
pip install --src . moexalgo[pandas]
# Подключение виртуального окружения в Jupyter Notebook
pip install ipykernel 
python -m ipykernel install --user --name=moexalgo 
```
После этого в Jupyter Notebook должен появится ярлык `moexalgo`. Если выбрать это ядро
jupiter notebook запустится из виртуального окружения с установленным пакетом `moexalgo`, 
и можно будет пробовать примеры `sample/sample.ipynb`. Более подробно про [подключение виртуального окружения к нотебуку тут](https://janakiev.com/blog/jupyter-virtual-envs/).