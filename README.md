# my_own_namespace.yandex_cloud_elk

A collection containing a custom Ansible module (`my_own_module`) and a role (`my_own_role`).

## Modules

### my_own_module

Creates a text file on the remote host at a specified path with specified content.

Options:
- `path` (required) - path to the file
- `content` (required) - content to write

## Roles

### my_own_role

A single task role that uses `my_own_module` with configurable defaults.

Role variables:
- `my_own_module_path` (default: `/tmp/default_path.txt`)
- `my_own_module_content` (default: `Default content`)
