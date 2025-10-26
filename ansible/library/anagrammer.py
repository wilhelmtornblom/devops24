from ansible.module_utils.basic import AnsibleModule

def reverse_string(text):
    """Reverse the input text"""
    return text[::-1]

def run_module():

    module_args = dict(
        message=dict(type='str', required=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    message = module.params['message']

    reversed_message=reverse_string(message)

    changed = (message != reversed_message)

    if message == "fail me":
        module.fail_json(
            msg="You requested this to fail",
            original_message=message,
            reversed_message=reversed_message,
            changed=changed
        )
    
    result = dict(
        changed=changed,
        original_message=message,
        reversed_message=reversed_message
    )
    
    module.exit_json(**result)

def main():
    run_module()

if __name__=="__main__":
    main()

