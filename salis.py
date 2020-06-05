import os
import pathlib
import subprocess



SECRET_PATH = str(pathlib.Path.home()) + "/.salis"
TEMPLATE = str(os.getcwd()) + "/assets/blank"
FINGER = str(os.getcwd()) + "/assets/fingerprint"
HELP = str(os.getcwd()) + "/assets/docs"



def prompt():
    while True:
        cmd = input("\n  > ")

        if not cmd.isalpha():
            reset()
            continue
        elif cmd == "clear":
            reset()
        elif cmd == "help":
            help()
        elif cmd == "ls":
            list_secrets()
        elif cmd == "key":
            set_fingerprint()
        elif cmd == "exit":
            break
        elif cmd == "plaintext":
            continue
        else:
            get_secret(cmd)



def format_print(str, n):
    print("\n" + "  " * n + str)



def reset(clear=True):
    global secrets 
    secrets = check_dir(SECRET_PATH)

    if clear:
        os.system("clear")
        format_print("salis secret stuff manager", 1)
        format_print("You have " + str(len(secrets)) + " secrets.", 2)



def help():
    with open(HELP) as help_file:
        content = help_file.read()
        print(content)



def list_secrets():
    reset(False)
    print()
    for secret in sorted(secrets):
        print("    " + secret)
    print()



def get_fingerprint():
    path = str(os.getcwd()) + "/.fingerprint"
    if os.path.exists(path):
        with open(path) as fingerprint_file:
            first_line = fingerprint_file.readline()
            return first_line.strip()
    else:
        return ""



def set_fingerprint():
    format_print("Please input your GPG key's fingerprint. (" + get_fingerprint() + ")", 2)
   
    target = str(os.getcwd()) + "/.fingerprint"
    os.system("cp " + FINGER + " " + target)
    os.system("nano " + target)

    with open(target) as fingerprint_file:
        first_line = fingerprint_file.readline().strip()

    format_print("Using key " + first_line + ".", 2)



def check_dir(dir_path):
    if not os.path.isdir(dir_path):
        format_print("Created a new secret directory.", 2)
        os.mkdir(dir_path)
        set_fingerprint()
        return []
    else:
        contents = os.listdir(dir_path)
        return contents



def encrypt(target):
    tmp = target + "plaintext"
    os.system("mv " + target + " " + tmp)
    os.system("gpg --trust-model always --output " + target + " --encrypt --recipient " + get_fingerprint() + " " + tmp + " > /dev/null")
    os.system("rm " + tmp)



def decrypt(target):
    tmp = target + "plaintext"
    os.system("gpg --output " + tmp + " --decrypt " + target + " 2> /dev/null")
    return tmp



def sanitize_secrets():
    secrets = os.listdir(SECRET_PATH)

    for secret in secrets:
        if "plaintext" in secret:
            os.system("rm " + SECRET_PATH + "/" + secret)



def secret_action(secret, action):
    action = action.lower()
    if action == "c":
        secret = decrypt(secret)

        with open(secret) as secret_file:
            password = secret_file.readline()
            copy_cmd = "echo " + password.strip() + " | xclip -selection clipboard"
            subprocess.check_call(copy_cmd, shell=True)

        format_print("Password copied to clipboard.", 2)

    elif action == "o":
        tmp = decrypt(secret)
        os.system("nano " + tmp)
        format_print("Secret opened.", 2)
        os.system("mv " + tmp + " " + secret)
        encrypt(secret)

    elif action == "d":
        os.system("rm " + secret)
        format_print("Secret deleted.", 2)

    else:
        format_print("Invalid option.", 2)

    sanitize_secrets()



def get_secret(secret):
    secret = secret.lower()
    target = SECRET_PATH + "/" + secret
    if not secret in secrets:
        os.system("cp " + TEMPLATE + " " + target)
        os.system("nano " + target)
        
        with open(target) as secret_file:
            first_line = secret_file.readline()

        if len(first_line) <= 1:
            os.system("rm " + target)
            format_print("No password given. Cancelling.", 2)
        else:
            encrypt(target)
            format_print("Created a new secret " + secret + ".", 2)

    else:
        format_print("Select action ([C]opy/[O]pen/[D]elete) for secret " + secret + ".", 2)
        sub_cmd = input("\n  > ")
        secret_action(target, sub_cmd)

    reset(False)



def main():
    reset()
    prompt()



main()