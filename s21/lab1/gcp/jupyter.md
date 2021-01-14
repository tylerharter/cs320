# Jupyter

1. Connect via SSH (or the Google Cloud Console) to your virtual machine.

2. Before we install Jupyter, let's get pip.  Run the following, and enter "Y" when prompted:

```
sudo apt update
sudo apt upgrade
sudo apt install python3-pip
```

The `apt` program lets you install software on an Ubuntu system; think
of it like `pip`, for more general (you can install stuff not related
to Python).  Putting `sudo` in front of the command means "do this as
a super user".  You're signed in as a regular user, without permission
to install software by default, so you'll use `sudo` often for
installing tools and other tasks.

3. Now let's use pip3 to install Jupyter (don't use sudo for this one):

`pip3 install jupyter`

4. When you start Jupyter notebook remotely, you'll want to set a
password for connecting to it.  Make it a good one, or anybody will be
able to take over your VM! (Whenever you need to enter something, like a password, 
in the terminal, don't worry if nothing is appearing as you're typing. Your keystrokes 
are still registering; the terminal just isn't displaying them!) 
Run the following:

```
mkdir -p ~/.jupyter
python3 -m notebook password
```

5. Now let's start Jupyter.  Run the following:

`nohup python3 -m notebook --no-browser --ip=0.0.0.0 --port=2020`

6. Now, open up a new browser window, and type `IP:2020` for the URL
(IP should be the External IP of the virtual machine).  You can enter
the same password that you set in step 4:

<img src="img/26.png" width=600>

7. After you login, make sure the setup works (e.g., you can create a
notebook and run code).

Good work on getting Jupyter running on your virtual machine!  We
suggest you bookmark the login page so you can come back to it later.
