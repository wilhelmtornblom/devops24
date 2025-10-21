# Examination 11 - Loops

Imagine that on the web server(s), the IT department wants a number of users accounts set up:

    alovelace
    aturing
    edijkstra
    ghopper

These requirements are also requests:

* `alovelace` and `ghopper` should be added to the `wheel` group.
* `aturing` should be added to the `tape` group
* `edijkstra` should be added to the `tcpdump` group.
* `alovelace` should be added to the `audio` and `video` groups.
* `ghopper` should be in the `audio` group, but not in the `video` group.

Also, the IT department, for some unknown reason, wants to copy a number of '\*.md' files
to the 'deploy' user's home directory on the `db` machine(s).

I recommend you use two different playbooks for these two tasks. Prefix them both with `11-` to
make it easy to see which examination it belongs to.

# QUESTION A

Write a playbook that uses loops to add these users, and adds them to their respective groups.

When your playbook is run, one should be able to do this on the webserver:

    [deploy@webserver ~]$ groups alovelace
    alovelace : alovelace wheel video audio
    [deploy@webserver ~]$ groups aturing
    aturing : aturing tape
    [deploy@webserver ~]$ groups edijkstra
    edijkstra : edijkstra tcpdump
    [deploy@webserver ~]$ groups ghopper
    ghopper : ghopper wheel audio

There are multiple ways to accomplish this, but keep in mind _idempotency_ and _maintainability_.

### QUESTION A Answer:
This is the playbook I created to first ensure that the groups exist and then add the users to their respective groups:
```
---

- name: Create groups and add users
  hosts: web
  become: true
  tasks:

    - name: Ensure groups exist
      ansible.builtin.group:
        name: "{{ item }}"
        state: present
      loop:
        - wheel
        - audio
        - video
        - tape
        - tcpdump

    - name: Create users and assign groups
      ansible.builtin.user:
        name: "{{ item.name }}"
        state: present
        groups: "{{ item.groups }}"
        append: yes
      loop:
        - { name: 'alovelace', groups: ['wheel', 'audio', 'video'] }
        - { name: 'ghopper',   groups: ['wheel', 'audio'] }
        - { name: 'aturing',   groups: ['tape'] }
        - { name: 'edijkstra', groups: ['tcpdump'] }
```
Its also really easy to add another user/group to the playbook if needed.

# QUESTION B

Write a playbook that uses

    with_fileglob: 'files/*.md5'

to copy all `\*.md` files in the `files/` directory to the `deploy` user's directory on the `db` server(s).

For now you can create empty files in the `files/` directory called anything as long as the suffix is `.md`:

    $ touch files/foo.md files/bar.md files/baz.md

### QUESTION B Answer:
This is the playbook I wrote to copy the files from my files/ folder to the deploy home folder:
```
---
- name: copy .md files
  hosts: db
  become: true
  tasks:
    - name: copy markdown files to deploy
      ansible.builtin.copy:
        src: "{{ item }}"
        dest: "/home/deploy"
        owner: deploy
        mode: 0600
      with_fileglob:
        - "files/*.md"
```



# BONUS QUESTION

Add a password to each user added to the playbook that creates the users. Do not write passwords in plain
text in the playbook, but use the password hash, or encrypt the passwords using `ansible-vault`.

There are various utilities that can output hashed passwords, check the FAQ for some pointers.

### BONUS QUESTION Answer:
First I began with install whois ``` sudo apt install whois ``` to be able to use mkpasswd to create a hashed password ``` mkpasswd --method=sha-512 ``` and I chose secretpassword as my password.
After that I created a .yml file called user-password.yml where I copied the hashed password in.
Then I encrypted the file with ansible vault: ``` ansible-vault encrypt user-password.yml ``` and after that I changed my ansible playbook to create users with the password from the user-password.yml file:
```
---

- name: Create groups and add users
  hosts: web
  become: true
  vars_files:
    - user-password.yml
  tasks:

    - name: Ensure groups exist
      ansible.builtin.group:
        name: "{{ item }}"
        state: present
      loop:
        - wheel
        - audio
        - video
        - tape
        - tcpdump

    - name: Create users and assign groups
      ansible.builtin.user:
        name: "{{ item.name }}"
        state: present
        groups: "{{ item.groups }}"
        append: yes
        password: "{{ password }}"
      loop:
        - { name: 'alovelace', groups: ['wheel', 'audio', 'video'] }
        - { name: 'ghopper',   groups: ['wheel', 'audio'] }
        - { name: 'aturing',   groups: ['tape'] }
        - { name: 'edijkstra', groups: ['tcpdump'] }
```
and for simplicity I entered the same vault password for this ansible-vault as I did for the previous one which is not recommended from a security perspective.
To run the playbook I ran the following command ``` ansible-playbook 11-add-users.yml --vault-password-file vault-password.txt ``` after the playbook ran successfully I confirmed that the passwords has been added to the users by going in to my web-server and typed su - alovelace and was prompted to type a password (secretpassword)


# BONUS BONUS QUESTION

Add the real names of the users we added earlier to the GECOS field of each account. Google is your friend.

# Resources and Documentation

* [loops](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)
* [ansible.builtin.user](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html)
* [ansible.builtin.fileglob](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fileglob_lookup.html)
* https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module

