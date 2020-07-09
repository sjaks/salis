# salis secret stuff manager
Salis is a program that managers passwords and other secret stuff.

- Uses GPG
- Commandline interface
- Easy to use
- Easy to sync

![](https://i.imgur.com/mu5KxOZ.png)

### Usage
Clone the repo
```
https://github.com/sjaks/salis.git
```
and run `python3 salis.py`. You will need to have a personal PGP key. Use command `key`. Run `help` to get a list of available commands.

#### Sync
The program creates a folder `~/.salis` and saves your secrets there GPG encrypted. You can sync that directory with a cloud storage or put it into a git repository. Or just save your secrets locally.
