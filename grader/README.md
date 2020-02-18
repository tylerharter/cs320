# Notes for Grading Tools

This is intended for staff use only. Students should not worry about this as it 
does not apply to them, nor is it maintained by them. As such any unauthorized pull requests 
regarding the autograder will be rejected. 

# Setup

Update your system:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove
```

Install git:

```
sudo apt-get install git
```

Install docker, preferably with snap (if on ubuntu):

```
sudo snap install docker
```

else: 

```
sudo apt-get install docker 
```

Make sure you have python3 (at least 3.6) installed with:

```
python3 -V
```

As well as pip3. If not install with:

```
sudo apt install python-pip3
```

If you haven't yet, clone this repo and navigate to this directory.
Let's install the python requirements with:

```
python3 -m pip install -r requirements.txt
```

At this point you should ne able to build the docker environment used to
run every submission. Before doing so, please go see the contents of 'DockerFile' 
and add/remove any dependencies that you might have. Build this image with (it'll take a while):

```
sudo docker build -t grader .
```

Now we need to add the s3 credentials for you to be able to read/write submissions.
You should have been provided with this. You need to write it in ~/.aws/credentials.

Finally, you should update `s3config.json` (or write your own!) for the 
s3interface to work properly. You will likely just need to change the profile name.

# Running the autograder

You can now try to run the autograder. If you aren't familiar with it's 
options try the following:

```
sudo python3 autograder.py -h
```

It should give you options like so:


```
usage: autograder.py [-h] [-s] [-d S3DIR] [-c] [-o | -k] [-sf STATS_FILE]
                     [-x [EXCLUDE [EXCLUDE ...]]] [-ff FORCE_FILENAME]
                     projects [projects ...] netid

Auto-grader for CS320

positional arguments:
  projects              id(s) of project to run autograder on.
  netid                 netid of student to run autograder on, or "?" for all
                        students.

optional arguments:
  -h, --help            show this help message and exit
  -s, --safe            run grader without uploading results to s3.
  -d S3DIR, --s3dir S3DIR
                        directory of local s3 caches.
  -c, --cleanup         remove temporary s3 dir after execution
  -o, --overwrite       rerun grader and overwrite any existing results.
  -k, --keepbest        rerun grader, only update result if better.
  -sf STATS_FILE, --statsfile STATS_FILE
                        save stats to file as a pickled dataframe
  -x [EXCLUDE [EXCLUDE ...]], --exclude [EXCLUDE [EXCLUDE ...]]
                        exclude files from being copied to codedir. Accepts
                        filenames or UNIX-style filename pattern matching. By
                        default README.md, main.ipynb, main.py are excluded
  -ff FORCE_FILENAME, --force-filename FORCE_FILENAME
                        force submission to have this filename

TIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov
```

_*Note:*_ Yes you should run the autograder with escalated priviledges. 
This is because it runs docker in the background and docker needs sudo 
access. In order to run the autograder without sudo you will need to follow
[these](https://docs.docker.com/install/linux/linux-postinstall/) 
instructions, but to do so you will need an admin.

Let's run the autograder in safe mode with the `-s` flag to see if everything is 
set up correctly:

```
sudo python3 autograder.py p1 ? -s
```

If everything ran smoothly you should see:

```
Found credentials in shared credentials file: ~/.aws/credentials
...list_objects...
========================================
<PATH_TO_SUBMISSION_FROM_S3DIR>.json
CONTAINER <LONG-DOCKER-CONTAINER-HEX-ID>
Score: <STUDENT'S-SCORE>
Did not upload results, running in safe mode
```

# Downloading submissions locally

This can be done by using `s3interface.py`'s CLI interface. Running it with 
the `-h` flag should give us more information about it:

```
usage: s3interface.py [-h] [-c CONFIG_PATH] [-ff FORCE_FILENAME]
                      projects [projects ...]                        

S3 Interface for CS320 

positional arguments:      
    projects              id(s) of project to download submissions for.

optional arguments:    
    -h, --help            show this help message and exit    
    -c CONFIG_PATH, --config CONFIG_PATH                     
                          S3 Configuration file path, default is ./s3config.json 
    -ff FORCE_FILENAME, --force-filename FORCE_FILENAME           
                          force submission to have this filename        

TIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov 
```

Therefore we should be able to download all submissions for p1 and p2 (for example) 
like so:

```
python3 s3interface.py p1 p2 -ff main.ipynb
```

_Note:_ This will require you to modify the config file or specify a new one. 

# Troubleshooting

### Errors while running the autograder

It is likely that the first time around the autograder will fail. This might be 
due to a large number of issues including:

* Missing dependencies
	* Fix: Update DockerFile and re-build image
* Missing file (ex: local import in student's code like lint.py)
	* Fix: Copy the missing file into the project folder
* Incorrect credentials
	* Fix: See with the professor, you most likely set up the s3 permissions wrong
* If using git in a project and there's an old/new mode change that stops you from 
changing branches without stashing. This happens because filemode (permissions) have changed.
	* Fix: run `git config --global core.filemode false`. Even with this, it might not work because it can be overwritten by the settings in `.git/config`.


## Tips and Tricks

* To open an interactive shell from a docker image (named grader in this case) 
you can run the following. Note that any changes will be discarded as a new 
container is created everytime.
	```
	sudo docker run -it grader bash
	```


## Changelog

* Feb 17, 2020: Created autograder config file `graderconfig.json`, 
Since the `Grader` inherits from `Database` the grader config gets 
merged with the s3 config. The grader's config takes precedence over 
s3's config so any keys in common will be overwriten.

* Feb 16, 2020: Split autograding logic from s3 logic, created 
new `s3interface.py` file and it's config file too. 

* Feb 11, 2020: Added README, updated requirements, fixed setup_codedir's 
permissions (file metadata wasn't copied), updated DockerFile.

* Feb 10, 2020: Forked from cs301/cs220's autograder. Renamed 
dockerUtil to autograder.
 
 
