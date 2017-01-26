# iperf-cron
Ansible playbook for deploying iperf as a cron job

iperf-cron will install iperf and register `iperf.py` as a cron task on each machine. iperf-cron also launches `iperf server` on each machine.

After that, `iperf.py` is running like a `iperf client`, which redirects the output of `iperf client` to log files.

You can configure the period of cron job in `group_vars/all`.

## Usage

#### 1. Launch

```bash
ansible-playbook -i hosts site.yml
```

This step registers the `iperf.py` to cron service.

#### 2. Collect 

```bash
ansible-playbook -i hosts collect.yml
```

#### 3. Clean Up

```bash 
ansible -i hosts -m shell -a "killall iperf"
ansible -i hosts -m shell -a "killall iperf.py"
ansible -i hosts -m shell -a "crontab -r"
```
