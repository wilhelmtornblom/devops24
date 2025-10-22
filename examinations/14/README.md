# Examination 14 - Firewalls (VG)

The IT security team has noticed that we do not have any firewalls enabled on the servers,
and thus ITSEC surmises that the servers are vulnerable to intruders and malware.

As a first step to appeasing them, we will install and enable `firewalld` and
enable the services needed for connecting to the web server(s) and the database server(s).

# QUESTION A

Create a playbook `14-firewall.yml` that utilizes the [ansible.posix.firewalld](https://docs.ansible.com/ansible/latest/collections/ansible/posix/firewalld_module.html) module to enable the following services in firewalld:

* On the webserver(s), `http` and `https`
* On the database servers(s), the `mysql`

You will need to install `firewalld` and `python3-firewall`, and you will need to enable
the `firewalld` service and have it running on all servers.

When the playbook is run, you should be able to do the following on each of the
servers:

## dbserver

    [deploy@dbserver ~]$ sudo cat /etc/firewalld/zones/public.xml
    <?xml version="1.0" encoding="utf-8"?>
    <zone>
      <short>Public</short>
      <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
      <service name="ssh"/>
      <service name="dhcpv6-client"/>
      <service name="cockpit"/>
      <service name="mysql"/>
    <forward/>
    </zone>

## webserver

    [deploy@webserver ~]$ sudo cat /etc/firewalld/zones/public.xml
    <?xml version="1.0" encoding="utf-8"?>
    <zone>
      <short>Public</short>
      <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
      <service name="ssh"/>
      <service name="dhcpv6-client"/>
      <service name="cockpit"/>
      <service name="https"/>
      <service name="http"/>
      <forward/>
    </zone>


### QUESTION A Answer:
First I began by adding the following tasks to my roles/webserver/tasks/main.xml.file 
```
- name: Ensure firewalld & python3-firewall are installed
  become: true
  ansible.builtin.package:
    name:
     - firewalld
     - python3-firewall
    state: present

- name: Enable and start firewalld
  become: true
  ansible.builtin.service:
    name: firewalld
    state: started
    enabled: yes

- name: Open HTTP & HTTPS in firewalld
  become: true
  ansible.posix.firewalld:
    service: "{{ item }}"
    permanent: yes
    state: enabled
    immediate: yes
  loop:
   - http
   - https
```
where I download firewalld & python3-firewall, start the firewalld service and then permanently enable the http & https service immediately if possible.

After that I added the following tasks to my roles/dbserver/tasks/main.xml file
```
---
# tasks file for dbserver
- name: Ensure firewalld & python3-firewall are installed
  become: true
  ansible.builtin.package:
    name:
      - firewalld
      - python3-firewall
    state: present

- name: Enable and start firewalld
  become: true
  ansible.builtin.service:
    name: firewalld
    state: started
    enabled: yes

- name: Open mariaDB in firewalld
  become: true
  ansible.posix.firewalld:
    service: mysql
    permanent: true
    state: enabled
    immediate: yes
```
that do the same thing but only to the mysql service.
and then I created the 14-firewall.yml playbook:
```
---
- name: COnfigure webserver
  hosts: web
  roles:
    - webserver

- name: Configure dbserver
  hosts: db
  roles:
    - dbserver
```
which ran successfully and then I confirmed that it had worked by going in to my dbserver and typing ``` sudo cat /etc/firewalld/zones/public.xml ``` and getting the same output as the example.




# Resources and Documentation

https://firewalld.org/
