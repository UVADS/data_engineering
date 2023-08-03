## Setting up AWS environment for linux, and docker
Instructions for setting an AWS EC2 instance running ubuntu, plus additionally loading docker and the Airflow image

The basic setup is the same for both.  We will use a small instance to explore linux, and then halfway through the course we'll repeat the sequence on a larger instance with enough resources to run Docker images.

## Basic Linux setup

## requirements
* create ssh key pair

* EC2
* Unbuntu LTS 10.4
* **t2.micro**
* use ssh key created earlier
* select your home ip
* connect via `ssh -i <path to key> ubuntu@<ip from ui>`

## !! Gotchas
* when you grab the ip for your instance, make sure you get the **public** not the **private** ip


## Setting up a larger instance with a larger capacity and loading Docker
Repeat the same instrauctions for the first instance, however we'll need to use a `t2.large` instance this time around.

* [GPG: GNU Privacy Guard](https://www.goanywhere.com/blog/what-is-gpg)

* `sudo apt update`

Next, install a few prerequisite packages which let apt use packages over HTTPS:
* `sudo apt install apt-transport-https ca-certificates curl software-properties-common`

Then add the GPG key for the official Docker repository to your system:
* `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`

Add the Docker repository to APT sources:
* `echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`

Update your existing list of packages again for the addition to be recognized:
* `sudo apt update`

Make sure you are about to install from the Docker repo instead of the default Ubuntu repo:
* `apt-cache policy docker-ce`

Finally, install Docker:
* `sudo apt install docker-ce`

Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it’s running:
* `sudo systemctl status docker`

* `sudo su -`
* `passwd ubuntu`
    - you will prompted for new password
    - re-enter password
    - exit
* `sudo su - ${USER}`
* You should now be able to run docker without having to use sudo

* `touch .env`
* Add these two lines
```
AIRFLOW_UID=50000
AIRFLOW_GID=0
```

setup airflow environment
```
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
first run
```
docker compose up airflow-init
```

```
docker-compose up
```

From another window session...
```
curl http://localhost:8080
```

Next: we need to open port 8080 to external traffic to see the UI

## links
* https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml
* https://stackoverflow.com/questions/69237178/how-to-set-up-correctly-environment-variables-for-airflow-using-docker-compose-i
* https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

```
error WARNING!!!: Not enough Disk space available for Docker.
At least 10 GBs recommended. You have 2.0G
```