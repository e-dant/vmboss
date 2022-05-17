#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(
    description="vmboss",
    epilog="A management utility for virtual machines",
)
parser.add_argument(
    "-m",
    dest="mode",
    metavar="mode",
    type=str,
    default=None,
    help='The mode, one of: "add", "remove", "start", "stop", or "query".',
)
parser.add_argument(
    "-d",
    dest="dry",
    action="store_true",
    default=False,
    help="If passed, only perform a dry-run.",
)
parser.add_argument(
    "-n",
    dest="vm_name",
    metavar="vm_name",
    type=str,
    default="primary",
    help="The pretty-name given to the vm.",
)
parser.add_argument(
    "-c",
    dest="vm_cpu_count",
    metavar="vm_cpu_count",
    type=int,
    default=5,
    help="The number of CPU cores available to the vm.",
)
parser.add_argument(
    "-r",
    dest="vm_memory_gb",
    metavar="vm_memory_gb",
    type=int,
    default=5,
    help="The amount of memory, in gigabytes, available to the vm.",
)
parser.add_argument(
    "-s",
    dest="vm_disk_space_gb",
    metavar="vm_disk_space_gb",
    type=int,
    default=5,
    help="The amount of disk space, in gigabytes, allocated for the vm.",
)
parser.add_argument(
    "-k",
    dest="os_kernel",
    metavar="os_kernel",
    type=str,
    default="linux",
    help="The name of the kernel, such as 'Linux' or 'Darwin', given to the vm. Case insensitive.",
)
parser.add_argument(
    "-p",
    dest="os_name",
    metavar="os_name",
    type=str,
    default="ubuntu",
    help="The name of the operating system, such as 'Arch', 'MacOS' or 'Ubuntu', given to the vm. Case insensitive.",
)
parser.add_argument(
    "-v",
    dest="os_release",
    metavar="os_release",
    type=str,
    default="jammy",
    help="The specific release of the operating system to use, such as '22.04' or 'Trusty'.",
)

args = parser.parse_args()

vm_modal_command = ""
vm_engine = ""

if args.mode is not None:
    if args.mode == "add":
        if os.system("which multipass &>/dev/null") == 0:
            vm_engine = "multipass"
            vm_modal_command = """{_vm_engine} launch {_os_release} --name {_vm_name} --cpus {_vm_cpu_count} --mem {_vm_memory_gb}G --disk {_vm_disk_space_gb}G""".format(
                _vm_engine=vm_engine,
                _vm_name=args.vm_name,
                _vm_cpu_count=args.vm_cpu_count,
                _vm_memory_gb=args.vm_memory_gb,
                _vm_disk_space_gb=args.vm_disk_space_gb,
                _os_kernel=args.os_kernel,
                _os_name=args.os_name,
                _os_release=args.os_release,
            )
    elif args.mode == "remove":
        if os.system("which multipass &>/dev/null") == 0:
            vm_engine = "multipass"
            vm_modal_command = (
                """{_vm_engine} delete {_vm_name};{_vm_engine} purge""".format(
                    _vm_engine=vm_engine,
                    _vm_name=args.vm_name,
                )
            )
    elif args.mode == "start":
        if os.system("which multipass &>/dev/null") == 0:
            vm_engine = "multipass"
            vm_modal_command = """{_vm_engine} start {_vm_name}&&{_vm_engine} shell {_vm_name}""".format(
                _vm_engine=vm_engine,
                _vm_name=args.vm_name,
            )
    elif args.mode == "stop":
        if os.system("which multipass &>/dev/null") == 0:
            vm_engine = "multipass"
            vm_modal_command = """{_vm_engine} stop {_vm_name}""".format(
                _vm_engine=vm_engine,
                _vm_name=args.vm_name,
            )

    configuration_json_str = """"configuration": {{
    "os kernel": "{_os_kernel}",
    "os name": "{_os_name}",
    "os release": "{_os_release}"
    "vm cpu count": {_vm_cpu_count},
    "vm disk space gb": {_vm_disk_space_gb},
    "vm engine": "{_vm_engine}",
    "vm memory gb": {_vm_memory_gb},
    "vm modal command": "{_vm_modal_command}",
    "vm name": "{_vm_name}",
}}""".format(
        _vm_name=args.vm_name,
        _vm_engine=vm_engine,
        _vm_cpu_count=args.vm_cpu_count,
        _vm_memory_gb=args.vm_memory_gb,
        _vm_disk_space_gb=args.vm_disk_space_gb,
        _vm_modal_command=vm_modal_command,
        _os_kernel=args.os_kernel,
        _os_name=args.os_name,
        _os_release=args.os_release,
    )

    print(configuration_json_str)

    if args.dry is False:
        os.system(vm_modal_command)
#   else:
#       print("[dry-run]")
else:
    print("no mode provided")
