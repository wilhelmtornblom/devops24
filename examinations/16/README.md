# Examination 16 - Security Compliance Check

The ever-present IT security team were not content with just having us put firewall rules
on our servers. They also want our servers to pass CIS certifications.

# QUESTION A

Implement _at least_ 10 of the checks in the [CIS Security Benchmark](https://www.cisecurity.org/benchmark/almalinuxos_linux) for AlmaLinux 10 and run them on the virtual machines.

These checks should be run by a playbook called `16-compliance-check.yml`.

*Important*: The playbook should only _check_ or _assert_ the compliance status, not perform any changes.

Use Ansible facts, modules, and "safe" commands. Here is an example:

    ---
    - name: Security Compliance Checks
      hosts: all
      tasks:
        - name: check for telnet-server
          ansible.builtin.command:
            cmd: rpm -q telnet-server
            warn: false
          register: result
          changed_when: result.stdout != "package telnet-server is not installed"
          failed_when: result.changed

Again, the playbook should make *no changes* to the servers, only report.

Often, there are more elegant and practical ways to assert compliance. The example above is
taken more or less verbatim from the CIS Security Benchmark suite, but it is often considered
bad practice to run arbitrary commands through [ansible.builtin.command] or [ansible.builtin.shell]
if you can avoid it.

In this case, you _can_ avoid it, by using the [ansible.builtin.package_facts](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_facts_module.html).

In conjunction with the [ansible.builtin.assert](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/assert_module.html) module you have a toolset to accomplish the same thing, only more efficiently and in an Ansible-best-practice way.

For instance:

    ---
    - name: Security Compliance Checks
      hosts: all
      tasks:
        - name: Gather the package facts
          ansible.builtin.package_facts:

        - name: check for telnet-server
          ansible.builtin.assert:
            fail_msg: telnet-server package is installed
            success_msg: telnet-server package is not installed
            that: "'telnet-server' not in ansible_facts.packages"

It is up to you to implement the solution you feel works best.

### QUESTION A Answer:
I used ``` ansible.builtin.package_facts & ansible.builtin.service_facts ``` to get information about the packages and services running on the servers and the ``` ansible.builtin.assert ``` to print out if the task failed/passed the test. I also added ``` ignore_errors: true ``` to the tasks to make sure that the playbook would continue to run if a task failed. I think this approach is very clear and easy to read.

# BONUS QUESTION

If you implement these tasks within one or more roles, you will gain enlightenment and additional karma.

# Resources

For inspiration and as an example of an advanced project using Ansible for this, see for instance
https://github.com/ansible-lockdown/RHEL10-CIS. Do *NOT*, however, try to run this compliance check
on your virtual (or physical) machines. It will likely have unintended consequences, and may render
your operating system and/or virtual machine unreachable.
