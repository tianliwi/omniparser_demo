# omniparser_demo
# Setup

* Install venv
```
sudo sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.12-venv
```

* Setup venv
```
python3 -m venv venv
source venv/bin/activate
pip install .
```

* Install Jupyter (https://medium.com/@sayanghosh_49221/jupyter-notebook-in-windows-subsystem-for-linux-wsl-f075f7ec8691)
```
pip install jupyter
```
open bash and type:
```
nano ~/.bashrc
```
Find 'esac', add following command below
```
alias jupyter-notebook="~/.local/bin/jupyter-notebook --no-browser"
```
Update profile and start
```
source ~/.bashrc
jupyter notebook
```

* Download hugging face model
```
git clone https://huggingface.co/microsoft/OmniParser
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
git lfs pull
```

* Copy above model under weights/ folder