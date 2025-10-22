# Examination 13 - Handlers

In [Examination 5](../05/) we asked the question what the disadvantage is of restarting
a service every time a task is run, whether or not it's actually needed.

In order to minimize the amount of restarts and to enable a complex configuration to run
through all its steps before reloading or restarting anything, we can trigger a _handler_
to be run once when there is a notification of change.

Read up on [Ansible handlers](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html)

In the previous examination ([Examination 12](../12/)), we changed the structure of the project to two separate
roles, `webserver` and `dbserver`.

# QUESTION A

Make the necessary changes to the `webserver` role, so that `nginx` only reloads when it's configuration
has changed in a task, such as when we have changed a `server` stanza.

Also note the difference between `restarted` and `reloaded` in the [ansible.builtin.service](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html) module.

In order for `nginx` to pick up any configuration changes, it's enough to do a `reload` instead of
a full `restart`.


### QUESTION A Answer:
I started of my adding all the tasks from the latest webserver playbook (10-web-template.yml) to my main.yml-file in the tasks/ folder, then I added a task that reloads nginx to my main.yml-file in the handlers/ folder

``` 
- name: Reload nginx
  become: true
  ansible.builtin.service:
    name: nginx
    state: reloaded 
```

and made sure that I added ``` become:true ``` to the handler task because without it my 12-roles playbook would not run. I also added my index.html, https.conf and example.internal.conf to my files folder and the example.internal.confg.j2 to my templates folder. To see if my handler would trigger I changed my index.html-file and ran the 12-roles playbook.

```
TASK [roles/webserver : Copy from files/index.html to /var/www/example.internal/html/index.html] ***
changed: [192.168.121.36]

RUNNING HANDLER [roles/webserver : Reload nginx] *******************************
changed: [192.168.121.36]
```

Here we can see that the change was detected and the handler ran and then I ran the playbook again and got the following output to confirm that the handler would not run:

```
TASK [roles/webserver : Copy from files/index.html to /var/www/example.internal/html/index.html] ***
ok: [192.168.121.36]
```
