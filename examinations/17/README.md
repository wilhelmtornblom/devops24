# Examination 17 - sudo rules

In real life, passwordless sudo rules is a security concern. Most of the time, we want
to protect the switching of user identity through a password.

# QUESTION A

Create an Ansible role or playbook to remove the passwordless `sudo` rule for the `deploy`
user on your machines, but create a `sudo` rule to still be able to use `sudo` for everything,
but be required to enter a password.

On each virtual machine, the `deploy` user got its passwordless `sudo` rule from the Vagrant
bootstrap script, which placed it in `/etc/sudoers.d/deploy`.

Your solution should be able to have `deploy` connect to the host, make the change, and afterwards
be able to `sudo`, only this time with a password.

To be clear; we want to make sure that at no point should the `deploy` user be completely without
the ability to use `sudo`, since then we're pretty much locked out of our machines (save for using
Vagrant to connect to he machine and fix the problem).

*Tip*: Check out _validate_ in [ansible.builtin.lineinfile](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/lineinfile_module.html) to ensure a file can be parsed correctly (such as running `visudo --check`)
before being changed.

No password is set for the `deploy` user, so begin by setting the password to `hunter12`.

HINT: To construct a password hash (such as one for use in [ansible.builtin.user](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html), you can use the following command:

    $ openssl passwd -6 hunter12

This will give you a SHA512 password hash that you can use in the `password:` field.

You can verify this by trying to login to any of the nodes without the SSH key, but using the password
provided instead.

To be able to use the password when running the playbooks later, you must use the `--ask-become-pass`
option to `ansible` and `ansible-playbook` to provide the password. You can also place the password
in a file, like with `ansible-vault`, or have it encrypted via `ansible-vault`.

### QUESTION A Answer:
I started with creating a role called set_password where I first created a variable called ``` deploy_user: "deploy" ``` in the defaults/main.yml-file and I was going to create the variable       ``` deploy_password: "hunter12" ``` in there aswell but decided to put that variable in the vars/main.yml instead so that I could encrypt only the password variable instead of both.

I used the same vault password as I did for the examinations before so that I could use the vault-password.txt filer later which is not good from a security perspective but its easier to run the playbook that way.

When everything was set up I started writing the tasks
```
---
# tasks file for set_password
- name: Set password for deploy
  ansible.builtin.user:
    name: "{{ deploy_user }}"
    password: "{{ deploy_password }}"
    update_password: always

- name: Create sudoers rule with password requirement
  ansible.builtin.lineinfile:
    path: /etc/sudoers.d/deploy
    line: "{{ deploy_user }} ALL=(ALL:ALL) ALL"
    state: present
    create: yes
    mode: 0440
    validate: /usr/sbin/visudo -cf %s

- name: Remove passwordless sudo rule
  ansible.builtin.lineinfile:
    path: /etc/sudoers.d/deploy
    line: "{{ deploy_user }} ALL=(ALL) NOPASSWD: ALL"
    state: absent
    validate: /usr/sbin/visudo -cf %s
```
Where I began with setting the password for the deploy user and after that I added the sudoers rule and then I removed the passwordless rule. For both the task where I added a rule and removed one I added ``` validate: /usr/sbin/visudo -cf %s ``` to ensure that the file is correctly saved, preventing being locked out of the servers.

I ran the playbook ``` ansible-playbook 17-sudo-password.yml --vault-password-file vault-password.txt --ask-become-pass ``` and confirmed that the password worked and the ```/etc/sudoers.d/deploy ``` file was changed by going in to one of the servers and typing ``` sudo cat /etc/sudoers.d/deploy ```