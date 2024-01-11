# Netlink DPLL test container #

This repo helps to build a container image for netlink DPLL debug

## Bulid ##

```bash
export IMG='quay.io/redhat-partner-solutions/dpll-debug:0.1'
```
(replace with your repository)

```bash
podman build --no-cache -t $IMG -f Containerfile  . && podman push $IMG
```

## Hack ##
The [Containerfile](Containerfile) specifies two hacks done to the kernel tools here:

### 1. Add DPLL YNL spec

```
# Comment out this line when dpll.yaml will be upstream
COPY dpll.yaml /linux/Documentation/netlink/specs/dpll.yaml
```

### 2. Make monitoring call blocking

The upstream implementation of `ynl.py` opens the monitoring socket in non-blocking mode, which means that if there is no notification at the exact same moment you run the cli, it will exit.
If we want to wait for notifications, this hack must be done:

```
# Uncomment this line if you want cli to block while waiting on netlink notifications
RUN sed -i 's/, socket.MSG_DONTWAIT//g' lib/ynl.py 
```

## Use ##

```bash
sh-5.1# python3 cli.py --no-schema --spec /linux/Documentation/netlink/specs/dpll.yaml --dump device-get
[{'clock-id': 5799633565433967664,
  'id': 0,
  'lock-status': 'locked-ho-acq',
  'mode': 'automatic',
  'mode-supported': ['automatic'],
  'module-name': 'ice',
  'type': 'eec'},
 {'clock-id': 5799633565433967664,
  'id': 1,
  'lock-status': 'locked-ho-acq',
  'mode': 'automatic',
  'mode-supported': ['automatic'],
  'module-name': 'ice',
  'type': 'pps'},
 {'clock-id': 5799633565433966964,
  'id': 2,
  'lock-status': 'unlocked',
  'mode': 'automatic',
  'mode-supported': ['automatic'],
  'module-name': 'ice',
  'type': 'eec'},
 {'clock-id': 5799633565433966964,
  'id': 3,
  'lock-status': 'unlocked',
  'mode': 'automatic',
  'mode-supported': ['automatic'],
  'module-name': 'ice',
  'type': 'pps'}]

sh-5.1# python3 cli.py --spec /linux/Documentation/netlink/specs/dpll.yaml --subscribe monitor

```
The last command above will block waiting for a notification.
