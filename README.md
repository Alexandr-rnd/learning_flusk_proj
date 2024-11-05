# learning_flusk_proj
new project for learning back-end development
 
Что сделано:
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
