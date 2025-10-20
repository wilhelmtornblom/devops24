# Examination 7 - MariaDB installation

To make a dynamic web site, many use an SQL server to store the data for the web site.

[MariaDB](https://mariadb.org/) is an open-source relational SQL database that is good
to use for our purposes.

We can use a similar strategy as with the _nginx_ web server to install this
software onto the correct host(s). Create the playbook `07-mariadb.yml` with this content:

    ---
    - hosts: db
      become: true
      tasks:
        - name: Ensure MariaDB-server is installed.
          ansible.builtin.package:
            name: mariadb-server
            state: present

# QUESTION A

Make similar changes to this playbook that we did for the _nginx_ server, so that
the `mariadb` service starts automatically at boot, and is started when the playbook
is run.

### QUESTION A Answer:
I added the following task to start the service at boot and when the playbook is run:
```
    - name: Ensure that MariaDB is started at boot.
      ansible.builtin.service:
        name: mariadb
        enabled: true
        state: started
```

# QUESTION B

When you have run the playbook above successfully, how can you verify that the `mariadb`
service is started and is running?

### QUESTION B Answer:
You can do it in different ways, for example you can connect via SSH to the db server and type ``` systemctl status mariadb ```
or you can add the following two tasks in your ansible playbook and run it again:
```   
 - name: Gather service information
      ansible.builtin.service_facts:

    - name: Is MariaDB running
      ansible.builtin.debug:
        msg: MariaDB is running
      when: ansible_facts.services['mariadb.service'].state == "running"
```
where the "Is MariaDB running" task only runs if the mariadb.service is running on the db server.


# BONUS QUESTION

How many different ways can use come up with to verify that the `mariadb` service is running?

### BONUS QUESTION Answer:
Other then the two options I mentioned above I am not sure, you could check if port 3306 (the port that MariaDB runs on) is open which would confirm that it is most likely running.
