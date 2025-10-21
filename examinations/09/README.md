# Examination 9 - Use Ansible Vault for sensitive information

In the previous examination we set a password for the `webappuser`. To keep this password
in plain text in a playbook, or otherwise, is a huge security hole, especially
if we publish it to a public place like GitHub.

There is a way to keep sensitive information encrypted and unlocked at runtime with the
`ansible-vault` tool that comes with Ansible.

https://docs.ansible.com/ansible/latest/vault_guide/index.html

*IMPORTANT*: Keep a copy of the password for _unlocking_ the vault in plain text, so that
I can run the playbook without having to ask you for the password.

# QUESTION A

Make a copy of the playbook from the previous examination, call it `09-mariadb-password.yml`
and modify it so that the task that sets the password is injected via an Ansible variable,
instead of as a plain text string in the playbook.

### QUESTION A Answer:
First I began with adding a variable in my ansible playbook
```
  vars:
    password: ""
```
And after that I replaced the password that is written in plain text with:
```    - name: Create MariaDB User
      community.mysql.mysql_user:
        name: webappuser
        password: "{{ password }}"
        login_unix_socket: /var/lib/mysql/mysql.sock
        priv: 'webappdb.*:ALL'
        state: present
```
Thereafter I ran the ansible playbook command:
```
ansible-playbook 09-mariadb-password.yml -e "password=secretpassword"
```
Which sets the password-variable to secertpassword.
I can confirm that the password is set by going in to my DB-server and typing
```
mariadb -u webappuser -p
```
and typing secretpassword and it works so the password has been set.


# QUESTION B

When the [QUESTION A](#question-a) is solved, use `ansible-vault` to store the password in encrypted
form, and make it possible to run the playbook as before, but with the password as an
Ansible Vault secret instead.

### QUESTION B Answer:
First I created an encrypted file to use in my ansible playbook:
```
ansible-vault create --vault-id password-file@prompt password.yml
```
And after that I wrote my password inside of the file that was created ``` password: secretpassword ```thereafter I ensured that the password was encrypted by doing ```cat password.yml ```



```
- hosts: db
  become: true
  vars_files:
    - password.yml
```
thereafter I removed "secretpassword" in plain text and replaced it with the password variable:
```
    - name: Create MariaDB User
      community.mysql.mysql_user:
        name: webappuser
        password: "{{ password }}"
        login_unix_socket: /var/lib/mysql/mysql.sock
        priv: 'webappdb.*:ALL'
        state: present
```
And then I saved my vault password to a .txt file and ran the following ansible playbook to confirm that it worked ``` ansible-playbook 09-mariadb-password.yml --vault-password-file vault-password.txt ``` and after that I logged in to my DB-server and succesfully logged in with the user name and password.

```
mariadb -u webappuser -p
```
