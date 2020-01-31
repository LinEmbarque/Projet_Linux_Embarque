# Linux_Embarque_2020

Participants : 
- Osama Al Shuaibi
- Abdulaziz Al Sudais
- David Brellmann
- Aurélien Lebrun
- Anouat Mahla


Ce markdown contient les étapes de mise en place du projet, puis des instructions pour le mettre en marche. 

Ce projet permet de réaliser un client serveur entre un ordinateur et une carte RPI3 à laquelle on a branché une caméra et une led. La caméra renverra au client les photos prises à sa demande et la led s'allumera lors de l'envoi des photos.


## Mise en place

### Flasher la carte
Docker nous permet d'accéder au système d'exploitation précompilée : 
```
$ docker pull pblottiere/embsys-rpi3-buildroot-video
```
On crée un conteneur grâce aux commandes suivantes : 
```
$ docker pull pblottiere/embsys-rpi3-buildroot-video
$ docker run -it pblottiere/embsys-rpi3-buildroot-video /bin/bash
$ docker# cd /root
$ docker# ls
$ buildroot-precompiled-2017.08.tar.gz
$ docker# tar zxvf buildroot-precompiled-2017.08.tar.gz
```
On flashe ensuite la carte RPI3 : 
```
$ sudo mount /dev/XXX /mnt

$ docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/images/sdcard.img

$ sudo dd if=sdcard.img of=/dev/XXX

$ sudo umount /dev/XXX /mnt
```
En remplaçant XXX par le chemin de la carte.

Pour trouver ce chemin, vous pouvez par exemple utiliser "gparted".

On modifie alors le fichier 'config.txt' de la première partition en y ajoutant: 

```
start_x=1
gpu_mem=128
```


Par la suite, il nous faudra connaitre l'adresse IP de la carte afin de nous connecter aux serveurs caméra et LED. D'abord, il faut brancher la carte en éthernet au réseau. Ensuite, nous avons choisi de  brancher directement la carte à l'ordinateur via un adaptateur TTL USB. Dès lors, on accède à la carte via `gtkterm`, en séléctionnant le port USB et un baud rate de 115200, pour réaliser un `ifconfig`. 

### Compilation

Ce système est composé d'une Raspberry Pi et d'une caméra que l'on souhaite manipuler. Si nous voulons communiquer avec la caméra, on utilisera l'API V4L que nous allons chercher à installer.
On se place sur le docker mis en place précédemment et on effectue:

```
$ sudo apt-get install libjpeg-dev libv4l-dev autoconf automake libtool

$ git clone https://github.com/twam/v4l2grab.git

$ cd v4l2grab

$ ./autogen.sh

```

On commente "undef malloc" dans config.h.in
 
Ensuite on configure notre compilateur : 
```
$ export PATH=$PATH:/root/buildroot-precompiled-2017.08/output/host/bin/

$ ./configure --host=arm-linux
```

Après avoir prélablement récupéré nos fichiers sources sur ce git et à l'aide d'un docker cp, on met notre code (v4l2grab.c) sur le docker. 
Puis on compile : 
```
$ make
```

On récupère `v4l2grab` de docker à notre pc.

Finalement, on copie le `v4l2grab` compilé et `led_server.py` dans le dossier /root. 
Pour accéder à la carte, on monte d'abord la partition:

```
$ sudo mount /dev/XXX /mnt
```
On effectue notre copie, et on démonte la partition:

```
$ sudo umount /mnt
```
La carte est donc prête à être utilisée.

## Montage

Le montage réalisé est le suivant:

La carte rpi3 est branchée en éthernet au réseau, et à une led via le port GPIO17.

Le schéma de la carte rpi3 est le suivant:

<p align="center">
  <img src="https://github.com/LinEmbarque/Projet_Linux_Embarque.git/image/schema_rpi3.png" width="300" title="Github Logo">
</p>

Le schéma du montage led est le suivant:

<p align="center">
  <img src="https://github.com/LinEmbarque/Projet_Linux_Embarque.git/image/schema_led.png" width="300" title="Github Logo">
</p>

Voici une photo du montage final:

<p align="center">
  <img src="https://github.com/LinEmbarque/Projet_Linux_Embarque.git/image/schema_montage.jpg" width="300" title="Github Logo">
</p>

## Utilisation

La communication entre la carte et le client se fait par une communication ssh.

D'abord, dans deux terminaux : 
```
$ ssh user@ADRESSE_IP
```
Avec l'adresse IP obtenue précédemment. Le mot de passe est 'user1*'. 
Nous devons par la suite nous mettre en mode super utilisateur (mot de passe : 'root1*'): 

```
$ su
```
On charge le module bcm2835-v4l2

```
$ modprobe bcm2835-v4l2
```

On se place dans le dossier /root:

```
$ cd /root
```

Dans un terminal, on execute le serveur led :
```
$ python led_server
```

Dans l'autre terminal on lance le serveur de la caméra : 

```
$ ./v4l2grab
```

Enfin, dans le terminal client, on execute le client: 
```
$ python client
```

Il suffit alors de suivre les instructions affichées. (On utilisera "t" depuis le client pour prendre une photo et "q" pour arrêter le programme).


## Makefile

Le rôle d'un Makefile est d'automatiser certaines commandes pour l'installation ou le lancement de programme. Nous avons cherché à créer un Makefile qui n'a malheureusement pas beaucoup d'intérêts pour automatiser des procédures. En effet, l'automatisation est limitée par un nom de partition différent par exemple. Toutefois, nous en avons tout de même crée un. On y a définit deux règles : l'une pour l'installation et l'autre pour le lancement du client.
    make installation : Lorsque la carte SD est connectée à l'ordinateur on copie le script python du serveur led et l'executable v4l2grab compilé.
    make client : Lorsque l'on est branché à la carte en ethernet, lance le client (nécessite d'avoir lancé tous les serveurs préalablement).



