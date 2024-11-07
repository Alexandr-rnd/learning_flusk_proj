# learning_flusk_proj
new project for learning back-end development
 
Основной путь настройки проекта:
**установелен pyenv** 
    curl https://pyenv.run | bash

    nano ~/.zshrc     открыто 
        прописаны строки:
        export PATH="$HOME/.pyenv/bin:$PATH"
        eval "$(pyenv init --path)"
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
        сохранено 

    source ~/.zshrc

**установлен питон нужной версии**
pyenv install 3.10

pyenv local 3.10

**установка poetry**

curl -sSL https://install.python-poetry.org | python3 -

poetry init

**Используется линтер ruff**

проект использует базовые возможности flask  и flask-admid 

основные кейсы: 
    1 авторизация в админку  по "username" и "password" и проверка роли == 'Admin'
    2 создание пользователя через форму регистрации 
    3 CRUD с пользователями на форме админки связь с ролями 
    4 СRUD с ролями 
    5 CRUD с постави связанными с авторами 
