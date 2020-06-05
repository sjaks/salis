# salis secret stuff manager
Salis is a program that managers passwords and other secret stuff.

- Uses GPG
- Commandline interface
- Easy to use
- Easy to sync

### Usage
Clone the repo
```
https://github.com/sjaks/salis.git
```
and run `python3 salis.py`. You will need to have a personal PGP key and the program asks for its fingerprint on first boot. Run `help` to get a list of available commands.

#### Sync
The program creates a folder `~/.salis` and saves your secrets there GPG encrypted. You can sync that directory with a cloud storage or put it into a git repository. Or just save your secrets locally.
