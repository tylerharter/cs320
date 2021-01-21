# SSH Keys

You can find what is called your SSH public key by running the
following and copying the output:

```
cat ~/.ssh/id_rsa.pub
```

The above should succeed if you're running commands for this lab on
your laptop and you created an SSH key there for lab 1.  If, however,
you're connected to your virtual machine and running commands there
for this lab, you need to generate an SSH key on the virtual machine.
(Creating an SSH key on your laptop to connect to your virtual machine
is different than creating an SSH key on your virtual machine to
connect to other services, like GitHub).

So if `cat ~/.ssh/id_rsa.pub` fails, try creating an SSH key first
before retrying by running `ssh-keygen` and repeatedly hitting `ENTER`
to accept all the defaults (including an empty password).

After you've copied the output from the terminal, go to
https://github.com/settings/keys and click "New SSH key".

Name the key "cs320-vm" (or whatever you like, really) and past the
contents of `id_rsa.pub` to the "Key" box, as in the following
screenshot:

<img src="step2/2.png" width=600>

Click "Add SSH Key" to finish adding it.