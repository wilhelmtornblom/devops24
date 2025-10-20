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
First I created an encrypted string to use in my ansible playbook:
```
ansible-vault encrypt_string password 'secretpassword' --name password
```
And after that I created a varaible in my playbook that saved the encrypted password in the variable password:
```
  vars:
    password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          65666565316265653432323361356231653332326536393133646331613861663063386434663039
          3065363430636238303632656231363738303361653837360a306233633737653363356132303239
          64393663653436616165363036356662663634343335373139396266323338636362316333333761
          6565633833396639660a383262623638626333333963353066336537623131303133376162323065
          6362
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
And I can confirm that the password works by going in to the DB-server and typing:
```
mariadb -u webappuser -p
```
and logging in with "secretpassword"
