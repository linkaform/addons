# LinkaForm Addons

Small repo that lets you load complete modules to LinkaForm platform.

Addons by default are runned on the docker container with the image `linkaform/python3_lkf:latest`. Every script inside the addons are run on their specified container, we do recommend running them on the same container


### Running addons

For installing the addons, you can simulate what the server does on the installation process or the upgrade process by running inside the container. What the server doses is basically enter the addons folder and run `python ./` (arguments discuss later on the file) with this python will load the module running first the `__main__.py` file and continue from there on, Loading every `__init__.py` file on it's way that has being evoqued or import.

1. Go to you home folder, if you don't have a `lkf` folder create one, and then clone the repo
```
mkdir ~/lkf
cd ~/lkf
git clone git@github.com:linkaform/addons.git
```

The addons repo has the basic configuration and basic LinkaForm modules, the rest of the modules are added by the git submodule tool, see more on [https://git-scm.com/book/en/v2/Git-Tools-Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

You are welcome to manipulate the addons repo and make the installation process your own way. Also as you are adding your own submodules you should create your own branch at your own origin. This is because LinkaForm addons branches are restricted, but pull requests are encouraged. Making your own origin, lets you  manipulate the code at your free will and allows you to pull for upgrades and manage your own submodules at your own will.

If you want to have a warranty upgrade compatibility without any merge conflicts, we suggest leaving the core files as they are. If you detect a bug or want to contribute, more than welcome. We will revise all pull requests and add them to the official repo if our develop team agrees on it.

2. We recommend also cloning the `linkaform_api` and checkout to the `3.0` branch as this is the current branch as of this writing
```
cd ~/lkf
git clone git@github.com:linkaform/linkaform_api.git
cd linkaform_api
git checkout 3.0
```

> You should have docker installed on your computer


##### Basic configuration

Running addons by itself on the container. Here you are mouning you addons folder inside the container.

```
docker run   -w /srv/scripts/addons -v ~lkf/addons/:/srv/scripts/addons -v ~/lkf/custom/:/srv/custom --name addons -d linkaform/python3_lkf:develop sleep infinity && docker exec -it addons bash
```

##### Advance configuration

Running with Basic config +  with `linkaform_api` module and I also like to mouth my `bash_history`, it just makes my life easier.

```
docker run   -w /srv/scripts/addons -v ~lkf/addons/:/srv/scripts/addons -v ~/lkf/custom/:/srv/custom -v ~/lkf/linkaform_api/linkaform_api:/usr/local/lib/python3.7/site-packages/linkaform_api/  -v ~/.bash_history:/root/.bash_history --name addons -d linkaform/python3_lkf:develop sleep infinity && docker exec -it addons bash
```

#### Advance configuration script

Just a small script I like to place on you `~/bin/` folder for and easy start of you proyect.


1. Copy this lines

```bash
#!/bin/bash

cd ~/lkf/addons
containerID=$(docker ps | grep addons | awk '{print $1}')
echo "container ID" $containerID
if [ -z "$containerID" ]; then
   echo "creating new container"
   docker stop addons && docker rm addons
   docker run   -w /srv/scripts/ -v `pwd`:/srv/scripts/addons -v ~/lkf/custom/:/srv/custom -v ~/lkf/linkaform_api/linkaform_api:/usr/local/lib/python3.7/site-packages/linkaform_api/  -v ~/.bash_history:/root/.bash_history --name addons -d linkaform/python3_lkf:develop sleep infinity && docker exec -it addons bash

else
   echo "existing"
   docker exec -it $containerID bash ;
fi
```
2. Go to your `bin` home folder
```
cd ~/bin
```
> If you don't have a bin directory just make one with $ `mkdir ~/bin`


3. Create the addons file and give execution permission
```
vi addons
# paste the above bash script
# save and close the file
# change the permissions with
chmod a+x addons
```

4. Run the script
```
./addons
```

With this steps you should be up and running

I suggest placing our addons project inside a `lkf` dir inside your home file.

### Running with parameters

The `__main__.py` file will evaluate which modules are already installed, which are missing and which ones are being configured for installation or upgrade.

When you run the setup simply indicate which module is being installed and which one is upgraded. This is done by passing arguments separated by a `:` for example `install:module1 upgrade:module2` , here Linkaform will run the installation process for `module1` and upgrading the `module2` by running.

```
python ./ install:module1 upgrade:module2 install:module3
```


### The structure


