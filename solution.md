## Подготовка

Создал репозиторий `my_own_collection` на GitHub. Склонировал `ansible/ansible`, развернул venv, установил зависимости, выполнил `hacking/env-setup`.

Окружение готово. Дальше работа в нём.

## Что сделано

### 1. Создание модуля my_own_module.py

Модуль принимает два параметра: `path` (путь к файлу) и `content` (содержимое). Если файл уже существует с таким же содержимым - ничего не делает. Иначе - создаёт или перезаписывает.

### 2. Проверка локально (шаг 4)

```
$ echo '{"ANSIBLE_MODULE_ARGS": {"path": "/tmp/test_ansible.txt", "content": "Hello from module!"}}' | python my_own_module.py
{"changed": true, "path": "/tmp/test_ansible.txt", "content": "Hello from module!" ...}

$ cat /tmp/test_ansible.txt
Hello from module!
```

Повторный запуск - `changed: false`. Идемпотентность работает.

### 3. Single task playbook и идемпотентность (шаг 6)

Playbook:

```yaml
- hosts: localhost
  tasks:
    - name: Create a test file
      my_own_module:
        path: /tmp/test_playbook.txt
        content: "Created via playbook!"
```

Запуск:

```
$ ansible-playbook playbook.yml -i localhost, --connection=local
...
TASK [Create a test file with my_own_module] ***********************************
changed: [localhost]
```

Повторно - `ok: [localhost]`, `changed=0`. Idempotency.

После проверок вышел из виртуального окружения.

### 4. Создание collection

```bash
ansible-galaxy collection init my_own_namespace.yandex_cloud_elk
```

Модуль перенесён в `plugins/modules/`.

### 5. Single task role

Создана роль `my_own_role` с тасками, использующими модуль. Параметры вынесены в `defaults/main.yml`:

- `my_own_module_path` - `/tmp/default_path.txt`
- `my_own_module_content` - `Default content`

### 6. Playbook для роли

Playbook в корне collection подключает роль.

### 7. Сборка collection

```bash
ansible-galaxy collection build
```

Архив: `my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz`

### 8. Установка и проверка из архива (шаги 15-16)

Установка collection из локального архива:

```
$ ansible-galaxy collection install my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz --force
Installing 'my_own_namespace.yandex_cloud_elk:1.0.0' to '/home/alex/.ansible/collections/ansible_collections/my_own_namespace/yandex_cloud_elk'
my_own_namespace.yandex_cloud_elk:1.0.0 was installed successfully
```

Запуск playbook с ролью из установленной collection:

```
$ ansible-playbook playbook.yml -i localhost, --connection=local

PLAY [Test my_own_role from collection] ****************************************
...
TASK [my_own_namespace.yandex_cloud_elk.my_own_role : Create file using my_own_module] ***
changed: [localhost]

PLAY RECAP *********************************************************************
localhost                  : ok=2    changed=1
```

Повторный запуск - `changed=0`. Collection работает, идемпотентность на месте.

### 9. Репозиторий и тег

Collection запушена в https://github.com/Chipy1/my_own_collection, тег v1.0.0.

## Ссылки

Collection: https://github.com/Chipy1/my_own_collection
Архив: https://github.com/Chipy1/my_own_collection/blob/main/my_own_namespace-yandex_cloud_elk-1.0.0.tar.gz
Playbook для роли: https://github.com/Chipy1/my_own_collection/blob/main/playbook.yml
Решение: https://github.com/Chipy1/my_own_collection/blob/main/solution.md

## Что пошло не так

Сначала не мог найти `hacking/test-module` - в свежей версии Ansible его убрали. Пришлось тестировать модуль через прямой вызов с JSON на stdin.

`hacking/env-setup` не до конца настроил PYTHONPATH - пришлось руками добавлять `lib` и `test/lib`, иначе модуль не видел `ansible.module_utils`.

`deactivate` внутри bash скрипта не сработал (отдельный процесс), пришлось просто закрыть терминал.

Коллекция собралась с первой попытки, что приятно удивило.
