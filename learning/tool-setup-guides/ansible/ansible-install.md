# Installation and Configure Ansible on Ubuntu

![Ansible](https://imgur.com/5HTcLFJ.png)

To install and configure Ansible on Ubuntu, you can follow these steps. Ansible is an open-source automation tool that simplifies configuration management, application deployment, and task automation.

**Step 1: Update Package Lists**

First, make sure your package lists are up to date:

```bash
sudo apt update
```

**Step 2: Install Ansible**

You can install Ansible directly from the official Ubuntu repositories using the following command:

```bash
sudo apt install -y ansible
```

**Step 3: Verify Ansible Installation**

After the installation is complete, you can verify that Ansible is installed by checking its version:

```bash
ansible --version
```

This should display the Ansible version and some configuration information.

**Step 4: Create an Ansible Configuration File (Optional)**

You can create an Ansible configuration file to customize Ansible behavior. The configuration file is usually named `ansible.cfg` and can be placed in the `/etc/ansible/` directory or in the current user's home directory. Here's how to create one in your home directory:

```bash
nano ~/.ansible.cfg
```

You can add configuration settings as needed. For example, you might want to specify the location of your inventory file or enable SSH agent forwarding:

```ini
[defaults]
inventory = ~/ansible/inventory
ssh_args = -o ForwardAgent=yes
```

Save the file and exit the text editor.

**Step 5: Create an Inventory File**

Ansible uses inventory files to specify the hosts it will manage. By default, Ansible looks for the inventory file at `/etc/ansible/hosts`. You can create your own inventory file with your target hosts. Here's an example:

```ini
[web]
webserver1 ansible_host=192.168.1.101
webserver2 ansible_host=192.168.1.102

[db]
dbserver ansible_host=192.168.1.103

[all:vars]
ansible_user=your_remote_username
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

Replace the IP addresses and `your_remote_username` with your actual values. This example defines two groups of hosts: `[web]` and `[db]`. The `[all:vars]` section includes default SSH settings.

**Step 6: Test Ansible**

You can test Ansible by running a simple ad-hoc command. For example, let's check if all hosts in the `[web]` group are reachable:

```bash
ansible web -m ping
```

This should return a "pong" message for each host if they are reachable.

**Step 7: Create Ansible Playbooks (Optional)**

While ad-hoc commands are useful for quick tasks, Ansible's real power comes from creating playbooks for automation. Playbooks are written in YAML and define a series of tasks to be executed on remote hosts. Here's a basic example of a playbook that installs the Nginx web server:

```yaml
---
- name: Install Nginx
  hosts: web
  become: yes

  tasks:
    - name: Update apt package cache
      apt:
        update_cache: yes

    - name: Install Nginx
      apt:
        name: nginx
        state: present

    - name: Start Nginx service
      service:
        name: nginx
        state: started
        enabled: yes
```

You can save this playbook in a `.yml` file (e.g., `nginx-install.yml`) and run it using the `ansible-playbook` command:

```bash
ansible-playbook nginx-install.yml
```

This playbook will install Nginx on all hosts in the `[web]` group.

You've now successfully installed and configured Ansible on Ubuntu. You can continue to create more playbooks to automate various tasks on your infrastructure.

## By [Harshhaa](https://www.github.com/NotHarshhaa)
