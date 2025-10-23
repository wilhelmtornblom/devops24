# Examination 15 - Metrics (VG)

[Prometheus](https://prometheus.io/) is a powerful application used for event monitoring and alerting.

[Node Exporter](https://prometheus.io/docs/guides/node-exporter/) collects metrics for Prometheus from
the hardware and the kernel on a machine (virtual or not).

Start by running the Prometheus server and a Node Exporter in containers on your Ansible controller
(the you're running Ansible playbooks from). This can be accomplished with the [prometheus.yml](prometheus.yml)
playbook.

You may need to install [podman](https://podman.io/docs/installation) first.

If everything worked correctly, you should see the data exported from Node Exporter on http://localhost:9090/,
and you can browse this page in a web browser.

# QUESTION A

Make an Ansible playbook, `15-node_exporter.yml` that installs [Node Exporter](https://prometheus.io/download/#node_exporter)
on each of the VMs to export/expose metrics to Prometheus.

Node exporter should be running as a `systemd` service on each of the virtual machines, and
start automatically at boot.

You can find `systemd` unit files that you can use [here](https://github.com/prometheus/node_exporter/tree/master/examples/systemd), along with the requirements regarding users and permissions.

Consider the requirements carefully, and use Ansible modules to create the user, directories, copy files,
etc.

Also, consider the firewall configuration we implemented earlier, and make sure we can talk to the node
exporter port.

HINT: To get the `firewalld` service names available in `firewalld`, you can use

    $ firewall-cmd --get-services

on the `firewalld`-enabled hosts.

Note also that while running the `podman` containers on your host, you may sometimes need to stop and
start them.

    $ podman pod stop prometheus

and

    $ podman pod start prometheus

will get you on the right track, for instance if you've changed any of the Prometheus configuration.

### QUESTION A Answer:
First I began with downloading podman and running the prometheus.yml playbook.

Next I created a new role under roles/ called node_explorer.

1. Defaults
I started by adding the variables I need to my default/main.yml-file
```
---
# defaults file for node_exporter
node_exporter_version: "1.8.2"
node_exporter_user: "node_exporter"
node_exporter_group: "node_exporter"
node_exporter_bin_path: "/usr/local/bin/node_exporter"
node_exporter_host: "0.0.0.0"
node_exporter_port: "9100"
node_exporter_options: ""
node_exporter_restart: "on-failure"
node_exporter_download_url: "https://github.com/prometheus/node_exporter/releases/download/v{{ node_exporter_version }}/node_exporter-{{ node_exporter_version }}.linux-amd64.tar.gz"
```

2. Templates
Then I created a jinja template for the Node Exporter service 
```
[Unit]
Description=Node Exporter

[Service]
User={{ node_exporter_user }}
ExecStart={{ node_exporter_bin_path }} --web.listen-address={{ node_exporter_host }}:{{ node_exporter_port }}
Restart={{ node_exporter_restart }}

[Install]
WantedBy=multi-user.target
```
where I use the variables from my defaults to tell the serivce the user, what ip-address to listen to and when to restart.

3. Handlers
And after that I added a simple handler that restarts node_exporter 
```
---
# handlers file for node_exporter
- name: Restart node_exporter
  ansible.builtin.systemd:
    name: node_exporter
    state: restarted
    daemon_reload: true
```
4. Tasks
And when that was done I started working on the tasks, I began by creating one that created the group, user and then I downloaded the Node Exporter and extracted it to the /tmp folder and after that a task that create a systemd service and the task after that starts the service.
And the last task I created was to allow node exporter through the firewall
```
- name: Allow Node Exporter firewall
  ansible.posix.firewalld:
    port: 9100/tcp
    permanent: true
    state: enabled
    immediate: true
```
And then I created the 15-node_exporter.yml playbook:
```
---
- name: Install Node Exporter on all servers
  hosts: all
  become: true
  roles:
    - node_exporter
```
And when I ran the playbook the first time it went smoothly with no errors and the node exporter service was active on both servers, but when I went to localhost:9090/targets it said that prometheus was not able to reach the db or webserver.
The solution to this problem was to replace the dbserver and webserver lines with the ip-adresses in the prometheus.yml playbook and rerun it:
```
            - targets:
                - 'node-exporter:9100'
                - 'webserver_ip:9100'
                - 'database_ip:9100'
```


# Resources and Information

* https://github.com/prometheus/node_exporter/tree/master/examples/systemd
* https://prometheus.io/docs/guides/node-exporter/
