# LinkaForm Addons

Small repo that lets you load complete modules to LinkaForm platform.

Addons by default are runned on the docker container with the image `linkaform/python3_lkf:latest`. Every script inside the addons are run on their specified container, we do recommend running them on the same container


### Downloding LinkaForm Addons

For installing the addons, you can simulate what the server does on the installation process or the upgrade process by running inside the container. What the server doses is basically enter the addons folder and run `python ./` (arguments discuss later on the file) with this python will load the module running first the `__main__.py` file and continue from there on, Loading every `__init__.py` file on it's way that has being evoqued or import.

1. Go to you home folder, if you don't have a `lkf` folder create one, and then clone the repo
```
mkdir ~/lkf
cd ~/lkf
git clone git@github.com:linkaform/addons.git
```
or use http:
`https://github.com/linkaform/addons.git`

The addons repo has the basic configuration and basic LinkaForm modules, the rest of the modules are added as submodules. To know more about how to use submodules tool, see more on [https://git-scm.com/book/en/v2/Git-Tools-Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

### Downloding LinkaForm Modules

LinkaForm modules are configure as submodules, to download modules as submodule just run:

```
git submodule update --init modules
git fetch --recurse-submodules
git pull --recurse-submodule
git submodule foreach --recursive git checkout main
```

This will download Linkaform Modules and place you at the main branch where all the development is currently being made. Specific branches are available for you to serach try and use.

Your are welcome to manipulate the addons repo and make the installation process your own way. Also as you are adding your own submodules you should create your own branch at your own origin. This is because LinkaForm addons branches are restricted, but pull requests are encouraged. Making your own origin, lets you  manipulate the code at your free will and allows you to pull for upgrades and manage your own submodules at your own will.

If you want to have a warranty upgrade compatibility without any merge conflicts, we suggest leaving the core files as they are. If you detect a bug or want to contribute, more than welcome. We will revise all pull requests and add them to the official repo if our develop team agrees on it.

2. We recommend also cloning the `linkaform_api` and checkout to the `3.0` branch as this is the current branch as of this writing
```
cd ~/lkf
git clone git@github.com:linkaform/linkaform_api.git
cd linkaform_api
git checkout 3.0
```

> You should have docker installed on your computer

### Configuring you Addons Settings

On the `config` folder there is a file called `settings.py` here are the baisc settings are ment to stay as they are. They are for basic configuration or for explanation purposes. You should create a file called `local_settings.py` on the same folder, this file is NOT uploaded to the repo, and here is where you place you sesitive information, this information is designe to live only on your local computer. All other sesitive information that you like will go here

`local_settings.py`
```python
# coding: utf-8
from  settings import * 
print('loading settings')


config.update({
            'USERNAME' : 'your_likaform_username@here.com',
            'APIKEY': 'your_APIKEY_HERE', 
})


``` 

# Requirments

Docker and Git, I asume you have `git` install so let's install docker.

## Installing Docker & Docker-compose

Docker installation instrucctions can be found here https://docs.docker.com/get-docker/#server follow the instruccions depending on your OS. Here I'a going to leave the instructions for installing docker on ubuntu.

- docker 
  https://docs.docker.com/install/#server
- docker-compose
  https://docs.docker.com/compose/install/

## Installing docker on ubuntu

https://docs.docker.com/desktop/install/ubuntu/


```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

```

To install the latest version, run:

```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

This will install the docker engine and the docker-compose plugin


### Give your user docker capabilities
sudo usermod -aG docker $USER

### Running Addons

As mention above, LinkaForm Addons run un Docker enviorment. This help us getting to work really fast. For that we have build a is a small shell util that is desing to help you run you addons containers in an easy way. You are welcome to use docker regular commands to run you enviorment, docker configuration can be found on the `docker` folder. More on this later.

You can find a file called `lkf` located on the root of the proyect, this is a small bash script that will run you `development enviorment` as well as you `testing enviorment`. 

First you need to be on the root of the proyect
`cd ~/lkf/addons`

Then you can start the proyect by running:
`./lkf start addons`

This will take a time the first time while it download all the addons layers. Hold it!!!

If everything run as expected, you shoud be placed inside the `modules` directory ready to start coding

`root@lkf-addons:/srv/scripts/addons/modules# `

### lkf util 

Getting to know the lkf util.

run: `./lkf -h`

```
Usage: lkf [options] <action[start|stop|build> <enviorment[addons|test|prod|dev>
    Special options:

      -i           load an specific image
      -a           load local linkaform_api as volume
      -r           relaod, alway need to be at the end of the options
      -c           works on build command, it runs the build command with no-cache
      -h           help!!!!

    Acction & Enviorment
      lkf <start|stop> addons     Starts the addons development environment
      lkf <start|stop> test       Starts the testing environment
      lkf build <prod|dev>      Starts the testing environment

```

#### Options

There are sevreal options that can be use as you run you enviorment

 -i loads a specific image with your addons, this is use if you need to run a particular version of the addons 
 -a this option will load the `linkaform_api` as a local volume so you can manupulate it.
 -r This option will reload the all you enviorment, a fresh start
 -c NO-CACHE build
 -h help

#### Actions

There are 3 actions, `start, stop , build` they are strait forward, they do just that 

#### Enviorment

- addons: This is the main developing enviorment, where you do your codeing
- test: This is an enviorment that includes pytest enviorment, so you can run all kind of testing, more on the `test` folder.
- prod:dev: This enviorment options are use for building purposes, so you can crate an image of your addons enviorment, this is use only if you are working on your own addons enviorment. Carefull, you need to specify this image name on your scripts. More on this on `lkf_addons` folder.

> Note: if you just install your docker enviorment, if you get a `docker.sock: connect:permission denied` you may need to open a new terminal. 


With this in mind, in summery your options are:

## RUNNING ADDONS

1. Running using default options
`./lkf start addons`

2. Running mounitng local `linkaform_api`
`./lkf -a start addons`

### Reloading

Depending you choice

`./lkf -r start addons` or `./lkf -ra start addons`

### Stoping 
`./lkf stop addons`


## Installing you modules on LinkaForm

Once you are up and running, you can **download, install and upgrade** LinkaForm modules using the `lkfaddons` util.

