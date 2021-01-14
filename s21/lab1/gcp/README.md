# Google Option for Virtual Machine

## Step 1: Signing up for GCP

Follow the instructions to [create a Google Cloud account](gcp.md).
Be sure to activate Google's free credit (if available).

## Step 2: Configuring the Firewall

What is a firewall?  First, a little background.

Remember from CS 220/301 that a computer (typically) has an *IP address*
(something like 123.234.210.001), and other computers knowing that IP
address can communicate with programs running on that computer.

If there are multiple running programs, they are differentiated by
*port numbers*.  For example, sending a message to 123.234.210.001:220
sends a message to the program on port 220 running on a computer with
address 123.234.210.001 (note the `:` between the IP address and port
number).  Sending a message to 123.234.210.001:320 might send a
message to a different program on that same machine.  Analogy: an IP
address is like the address of an apartment building (the computer),
and a port number is like the apartment number of a specific unit;
programs are the residents living in the units.

A Firewall (among other things) can block access to certain ports for
outsiders, to provide security.  We will unblock all ports for our
virtual machine.  This is not the most secure option, but it is
convenient, and fine for the purposes of this course.

Follow [these instructions](firewall.md) to configure the firewall to unblock all
ports.

## Step 3 [Recommended]: Creating an SSH Key

You already have an idea of what a shell is: you've been either using
PowerShell (Windows) or bash (default on Mac) in CS 220/301.  *ssh*
stands for "secure shell", and it's a special shell that lets you
remotely connect to other computers over the network and run commands
there.  An *ssh key* is like a randomly generated password that ssh
automatically uses to access other machines (you won't generally type
it).

Macs and recent Windows computers (Windows 10 with recent updates)
should have a program OpenSSH installed, which will be the most
convenient way to access your virtual machine.

Try [these directions](ssh.md) to create an SSH key and connect it
with your cloud account.  If it doesn't work (e.g., because you don't
have OpenSSH), don't worry too much -- there are workarounds later.

## Step 4: Launching your Virtual Machine

Now it's time to actually create your virtual machine!  Follow [these steps](launch.md).

## Step 5a: Connecting with SSH from your terminal

If you were able to configure the SSH key properly in Step 3, follow
[these directions](connect.md).

## Step 5b [Alternative]: Connecting without SSH

If you couldn't configure the SSH key, follow [these
directions](connect-alt.md) instead.

## Step 6: Setting up Jupyter

Now lets get Jupyter and some other software installed.  Follow [these
directions](jupyter.md).

