# Examination 18 - Write an Ansible module (VG)

Ansible modules are types of plugins that execute automation tasks on a 'target'. In the previous
examinations you have used many different modules, written by Ansible developers.

A module in Ansible is a Python script that adheres to a particular convention.

You can see the places where Ansible looks for modules by dumping the Ansible configuration
and then search for `DEFAULT_MODULE_PATH`:

    $ ansible-config dump | grep -i module_path

We will now write our own module, and run it through Ansible.

# QUESTION A

Look at [Developing modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
and create a module that

* Is called `anagrammer`
* Takes one parameter, `message`, that is a string.
* Returns two values:
    - `original_message` that is the string that is passed through `message`
    - `reversed_message` that is the `message` string, only backwards (reversed).
* If the `original_message` and `reversed_message` is different, the `changed` parameter should be `True`, otherwise
  it should be `False`.

When you are done, you should be able to do

    $ ANSIBLE_LIBRARY=./library ansible -m anagrammer -a 'message="hello world"' localhost

And it should return

    localhost | CHANGED => {
        "changed": true,
        "original_message": "hello world",
        "reversed_message": "dlrow olleh"
    }

You should also be able to do

    ANSIBLE_LIBRARY=./library ansible -m anagrammer -a 'message="sirap i paris"' localhost

And it should return

    localhost | SUCCESS => {
        "changed": false,
        "original_message": "sirap i paris",
        "reversed_message": "sirap i paris"
    }

If you pass in 'fail me', it should fail like this:

    localhost | FAILED! => {
        "changed": true,
        "msg": "You requested this to fail",
        "original_message": "fail me",
        "reversed_message": "em liaf"
    }

### QUESTION A Answer:
First I began with creating the library/ directory ``` mkdir -p library ``` where I created the anagrammer.py python file ``` nano anagrammer.py ``` and wrote three functions, one to reverse the input string, one to set up the ansible module and one to run the module. I also made the python file executable ``` chmod +x library/anagrammer.py ```.
I was able to run all the test cases and get the expected output.

# QUESTION B

Study the output of `ansible-config dump | grep -i module_path`. You will notice that there is a directory
in your home directory that Ansible looks for modules in.

Create that directory, and copy the Ansible module you just wrote there, then make a playbook
that uses this module with the correct parameters.

You don't need to worry about FQCN and namespaces in this examination.

### QUESTION B Answer:
I began with creating the module directory ``` mkdir -p ~/.ansible/plugins/modules ``` and copied the anagrammer.py file to it ``` cp library/anagrammer.py ~/.ansible/plugins/modules/ ``` then I created 18-anagrammer-test.yml playbook and wrote two tasks that uses the anagrammer module and two that outputs the result.

# QUESTION C

Create a playbook called `18-anagrammer.yml` that uses this module.

Make the playbook use a default variable for the message that can be overriden by using something like:

    $ ansible-playbook --verbose --extra-vars message='"This is a whole other message"' 18-custom-module.yml

### QUESTION C Answer:
I created the playbook and added the variable 
```
vars:
    message: "hello world"
``` 
to use as my default variable in the task
``` 
  tasks:
    - name: Run anagrammer
      anagrammer:
        message: "{{ message }}"
      register: result
```
so it is displayed if no message is added when you run the playbook. 
I was able to run the playbook with no added message and with the ``` ansible-playbook --verbose --extra-vars message='"This is a whole other message"' 18-custom-module.yml ``` command without any errors.

# BONUS QUESTION

What is the relationship between the booleans you can use in Python, and the various "truthy/falsy" values
you most often use in Ansible?

What modules/filters are there in Ansible that can safely test for "truthy/falsy" values, and return something
more stringent?
