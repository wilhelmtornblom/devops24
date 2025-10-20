# Examination 1 - Understanding SSH and public key authentication

Connect to one of the virtual lab machines through SSH, i.e.

    $ ssh -i deploy_key -l deploy webserver

Study the `.ssh` folder in the home directory of the `deploy` user:

    $ ls -ld ~/.ssh

Look at the contents of the `~/.ssh` directory:

    $ ls -la ~/.ssh/

## QUESTION A

What are the permissions of the `~/.ssh` directory?

Why are the permissions set in such a way?

### QUESTION A Answer:
The permissions for the .shh directory are read + write + execute for the owner of the folder while group and others have no permissions to the folder.

The permissions are set in that way to protect the SSH-keys from being accessed or modified by other users.

## QUESTION B

What does the file `~/.ssh/authorized_keys` contain?

### QUESTION B Answer:
The authorized_keys file contains public SSH-keys of remote users who are allowed to connect to the account via SSH.

## QUESTION C

When logged into one of the VMs, how can you connect to the
other VM without a password?

### QUESTION C Answer:
First you need to generate a SSH-key pair
```
ssh-keygen 
```
After that you can copy the public key to the other account and computer you want to connect to
```
ssh-copy-id deploy@webserver
```


### Hints:

* man ssh-keygen(1)
* ssh-copy-id(1) or use a text editor

## BONUS QUESTION

Can you run a command on a remote host via SSH? How?

### BONUS QUESTION Answer:
Yes, it is possible
```
ssh deploy@192.168.121.36 "cat .ssh/authorized_keys"

```
This command will print out all the public keys authorized to connect to the account.