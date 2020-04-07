# Notes for Grading Tools

This is intended for staff use only. Students should not worry about this as it 
does not apply to them, nor is it maintained by them. As such any unauthorized pull requests 
regarding the autograder will be rejected. 

# Overview

Currently the tools consist of two files:
* `s3interface.py`: This file contains the class `Database` which is responsible for 
interacting with the amazon s3 bucket that stores the submissions. It can also 
be used as a CLI to download the submissions locally for inspection and cheating detection.

* `autograder.py`: This file contains the class `Grader` which is a subclass of `Database`.
It is responsible for setting up the testing environment and directories, 
re-run every submission, run the test/tester on it, and upload the results. It also aggregates 
some basic statistics about the grades but this is still in the works. Finally, this can 
also be used as a CLI to run the autograder on a specific project or student. 

Both of these files use a json config file to store default configuration 
parameters. Any of these parameters can be overwritten at runtime through the 
CLI. 

_Note on Inheritance and Configuration:_ the base class's config will be merged with 
the subclass's config. Any parameters in the subclass will take precedence and overwrite 
the base class's config.  

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
sudo apt install python3-pip
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

### Autograder CLI

You can now try to run the autograder. If you aren't familiar with it's 
options try the following:

```
sudo python3 autograder.py -h
```

It should give you options like so:


```
usage: autograder.py [-h] [-cf GRADER_CONFIG_PATH] [-cfs3 S3_CONFIG_PATH] [-s]
                     [-d S3DIR] [-c] [-o | -k] [-sf STATS_FILE]
                     [-x [EXCLUDE [EXCLUDE ...]]] [-ff FORCE_FILENAME]
                     [-t TIMEOUT] [-tc TEST_CMD]
                     projects [projects ...] netid

Auto-grader for CS320

positional arguments:
  projects              id(s) of project to run autograder on.
  netid                 netid of student to run autograder on, or "?" for all
                        students.

optional arguments:
  -h, --help            show this help message and exit
  -cf GRADER_CONFIG_PATH, --config GRADER_CONFIG_PATH
                        autograder configuration file path, default is
                        ./graderconfig.json
  -cfs3 S3_CONFIG_PATH, --s3config S3_CONFIG_PATH
                        s3 configuration file path, default is ./s3config.json
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
  -t TIMEOUT, --timeout TIMEOUT
                        docker timeout in seconds
  -tc TEST_CMD, --test-cmd TEST_CMD
                        command that docker runs to test code. Should create a
                        result.json

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

### Autograder Crontab

Running the grader periodically is often desired. The simplest 
way of doing so it through a cronjob. 

For this to work you'll need to edit the `grader-daemon.sh` script 
in order to make sure it is running the autograder in the way you intend.

Further, you will need to be able to run the daemon without sudo 
privileges as crontabs run unprivileged and without your user. 
To account for this you will have to follow the directions above 
on how to run without sudo. You might also need to specify the full 
python path to use in the daemon script.

Once you have the `grader-daemon.sh` script running without sudo and 
how you intend it, you can simply add it as a cronjob. To do this run: 

```
crontab -e
```

And add something like so:

```
0 * * * * <PATH TO THE GRADER DIRECTORY>/grader-daemon.sh > cronlog.txt 
```

The `cronlog.txt` file will simply capture the output and help you debug
if anything goes awry. This is rather rudimentary as better logging methods exist 
but it works for now.

I highly suggest you check your crontab [here](https://crontab.guru/).


# Downloading submissions locally

This can be done by using `s3interface.py`'s CLI interface. Running it with 
the `-h` flag should give us more information about it:

```
usage: s3interface.py [-h] [-da | -dm | -dp] [-cf CONFIG_PATH]
                      [-ff FORCE_FILENAME] [-mf MOSS_FORMAT] [-p PREFIX]
                      [projects [projects ...]]

S3 Interface for CS320

positional arguments:
  projects              id(s) of project to download submissions for.

optional arguments:
  -h, --help            show this help message and exit
  -da, --download-all   download all submissions in an s3 file-structured way
  -dm, --download-moss  download all submissions in same directory using
                        moss_format as filename formatter, used for moss
                        cheating detection
  -dp, --download-prefix
                        download all s3 files that have the given prefix
  -cf CONFIG_PATH, --config CONFIG_PATH
                        s3 configuration file path, default is ./s3config.json
  -ff FORCE_FILENAME, --force-filename FORCE_FILENAME
                        force submission to have this filename
  -mf MOSS_FORMAT, --moss-format MOSS_FORMAT
                        filename format to use when downloading for moss
  -p PREFIX, --prefix PREFIX
                        download prefix to use

TIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov
```

Therefore we should be able to download all submissions for p1 and p2 (for example) 
like so:

```
python3 s3interface.py -da p1 p2
```

And you'll be able to download these in a moss-compatible format like so:

```
python3 s3interface.py -dm p1 p2
```

Finally you can download any files with `SNAP_ALLOWED_EXT` and with a 
given prefix ('b' in the example below) like so:

```
python3 s3interface.py -dp --prefix "b"
```

_Note:_ This will require you to modify the config file or specify a new one. 
For the moss download it will download then to the `MOSS_DIR` using the `MOSS_FORMAT` 
to name the file. This format string can take any arguments returned by `Database.parse_s3path`.

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

### Crontab not running/crashing

This might be due to a number of things, but I would recommend you first 
make sure you can run the daemon script manually and without sudo. 

# Tips and Tricks

* To open an interactive shell from a docker image (named grader in this case) 
you can run the following. Note that any changes will be discarded as a new 
container is created every time.
	```
	sudo docker run -it grader bash
	```
 
* You might want to also install the aws cli for quick debugging. 
You can do so with:
    ```
    sudo apt install awscli 
    ```

* Being familiar with docker can be helpful, a good docker cheat-sheet 
can be found [here](https://github.com/wsargent/docker-cheat-sheet).
Specifically, when rebuilding the docker image (after modifying the Dockerfile) 
it might be helpful to stop and remove all containers and delete all images like seen 
[here](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes). Be 
careful with these commands:
    ```
    docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)
    docker rmi $(docker images -a -q) 
    ```

# Changelog

* April 7, 2020: Added geopandas dependency pysal and it's dependency libspatialindex-c4v5 to Dockerfile.

* April 2, 2020: Added catch all and skipping logic if a single submission fails.

* March 11, 2020: Updated `Dockerfile` to include flask, html5lib, lxml.

* Feb 22, 2020: Added `test_cmd` and `result_file` config options to the grader.
Started removing old stats collector code. Added p2 to the daemon script. 
Added docs about daemonizing grader, and a prefix downloader in `s3interface.py` 
to download the snapshot directory (used to compute final grades).

* Feb 18, 2020: Updated DockerFile, added Moss download compatibility (see above).

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
 
 
# TODO

- [ ] Cleanup through docker to avoid permission denied errors
- [ ] Move conf over to yaml for easier configs
- [ ] Add per project configs, run-all command
- [ ] Add better logging (to a file)
- [ ] Add stats collector class
 
