# WARN: Some codes in this script SHOULD be improved!!!
import os
import json
import time


class Arch_installer:
    def __init__(self) -> None:
        self.system_packages = [
            "base",
            "base-devel",
            "linux-firmware",
            "networkmanager",
        ]
        pass

    def ask_partition_name(self, boot_partition, root_partition, swap):
        self.boot_partition = boot_partition
        self.root_partition = root_partition
        self.swap = swap

    def format_partitions(self):
        os.system(f"""mkfs.fat -F 32 {self.boot_partition}""")
        os.system(f"""mkfs.swap {self.swap}""")
        # ask user which type of popular filesystem to format
        fs_list = ["btrfs", "xfs", "ext4"]
        for item in fs_list:
            print(item)
        self.filesystem_type = input("Input the filesystem type you want: ")
        if self.filesystem_type == "btrfs":
            self.system_packages.append("btrfs-progs")
            # ask user whether pass arguments or not
            label = input(
                "If you want to set a label, please input it(or you can input `q` to exit): "
            )
            if label == "q":
                os.system(f"mkfs.btrfs {self.root_partition}")
            else:
                os.system(f"mkfs.btrfs -L {label} {self.root_partition}")
        elif self.filesystem_type == "xfs":
            self.system_packages.append("xfsprogs")
            # xfs is needing help to support user pass arguments while formatting it
            os.system(f"mkfs.xfs {self.root_partition}")
        elif self.filesystem_type == "ext4":
            os.system(f"mkfs.ext4 {self.root_partition}")

    # For btrfs special
    def btrfs_create_subvolume(self):
        if self.filesystem_type == "btrfs":
            # judge user if pass arguments
            confirm_argument = input(
                "Do you want to pass arguments while mounting? y/n "
            )
            if confirm_argument == "n":
                os.system(f"""mount -t btrfs {self.root_partition} /mnt""")
            elif confirm_argument == "y":
                arguments = input("Please input your arguments: ")
                os.system(
                    f"""mount -t btrfs -o {arguments} {self.root_partition} /mnt"""
                )
            # judge user if set subvolume name
            confirm_subvolume_name = input(
                "Do you want to set your subvolume name? y/n "
            )
            if confirm_subvolume_name == "y":
                subvolume_name_for_root = input(
                    "Input your subvolume name for *root* partition: "
                )
                subvolume_name_for_home = input(
                    "Input your subvolume name for *home* partition: "
                )
                os.system(f"btrfs subvolume create /mnt/{subvolume_name_for_root}")
                os.system(f"btrfs subvolume create /mnt/{subvolume_name_for_home}")
            else:
                os.system("btrfs subvolume create /mnt/@")
                os.system("btrfs subvolume create /mnt/@home")
            os.system("umount /mnt")
        else:
            pass

    def mount_system_partition(self):
        # judge user if pass argument
        confirm_argument = input("Do you want to pass your own argument? y/n ")
        if confirm_argument == "y":
            user_argument_for_root = input("Input your argument for root: ")
            user_argument_for_home = input(
                "Input your argument for home(subvol=/<home_subvolume_name>...): "
            )
            # mount root
            os.system(
                f"mount -t {self.filesystem_type} -o {user_argument_for_root} {self.root_partition} /mnt"
            )
            # mount home
            os.system("mkdir /mnt/home")
            os.system(
                f"mount -t {self.filesystem_type} -o {user_argument_for_home} {self.root_partition} /mnt/home"
            )
        else:
            os.system(f"mount {self.root_partition} /mnt")
            os.system(f"mount {self.root_partition} /mnt/home")
        os.system("mkdir /mnt/boot")
        os.system(f"""mount {self.boot_partition} /mnt/boot""")
        os.system(f"""swapon {self.swap}""")
        time.sleep(5)
        os.system("clear")

    def change_mirror(self):
        mirror_list = {
            "TsingHua": "Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch",
            "USTC": "Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch",
            "LZU": "Server = https://mirrors.lzu.edu.cn/archlinux/$repo/os/$arch",
            "HuaWei_Cloud": "Server = https://mirrors.huaweicloud.com/archlinux/$repo/os/$arch",
            "Ali_Cloud": "Server = http://mirrors.aliyun.com/archlinux/$repo/os/$arch",
        }
        for key in mirror_list.keys():
            print(key)
        mirror = input(
            "Choose one mirror provider above(Name should be the SAME as printed, upcase), if you want to use other, please input `o`: "
        )
        if mirror == "o":
            print(
                "The mirror url form is `Server = https://<mirror_domain>/archlinux/$repo/os/$arch`"
            )
            mirror = input("Now please input the mirror url: ")
        elif mirror not in mirror_list.keys():
            print(
                "Please input the correct name(Name should be the SAME as printed, upcase)"
            )
            mirror = input(
                "Choose one mirror provider above(Name should be the SAME as printed, upcase), if you want to use other, please input `o`: "
            )
            mirror = mirror_list[mirror]
        elif mirror in mirror_list.keys():
            mirror = mirror_list[mirror]
        os.system("cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.back")
        with open("/etc/pacman.d/mirrorlist", "w") as mirror_file:
            mirror_file.write(mirror)
        time.sleep(5)
        os.system("clear")

    def ask_packages_name_for_install(self):
        # For kernel
        print(
            "Please visit this page to choose a kernel: https://wiki.archlinuxcn.org/wiki/Kernel"
        )
        kernel_name = input(
            "Input your kernel package name to install(ONLY official repo supported!!!), input should be `linux(-...)`: "
        )
        self.system_packages.append(kernel_name)
        while True:
            packages_user_install = input(
                "Input package name you want to install(in official repo, no in AUR, input `q` to exit): "
            )
            if packages_user_install == "q":
                break
            else:
                self.system_packages.append(packages_user_install)

    def install_packages(self):
        for item in self.system_packages:
            os.system(f"pacstrap /mnt {item}")

    def genarate_fstab(self):
        os.system("genfstab -U /mnt > /mnt/etc/fstab")


def optional_mount_partition(willing):
    if willing == "y":
        os.system("lsblk -f")
        print(
            "Please input the partitions you want to mount(this will be mounted without arguments)!!!"
        )
        while True:
            to_be_mounted_partition = input(
                "Input(/dev/.... If you WANT to exit, please press`q` and return):"
            )
            if to_be_mounted_partition != "q":
                os.system(f"mount {to_be_mounted_partition}")
            elif to_be_mounted_partition == "q":
                break
    elif willing == "n":
        return
    else:
        print("Please input y/n")


def chroot():
    os.system("arch-chroot /mnt")


installer = Arch_installer()
installer.ask_partition_name(
    boot_partition=input("Input your boot partition:"),
    root_partition=input("Input your root partition:"),
    swap=input("Input your swap partition:"),
)
# TODO
installer.change_mirror()
installer.ask_packages_name_for_install()
installer.install_packages()
optional_mount_partition(input("Do you want to mount other partitions? y/n: "))
chroot()
# NOTE: This wanted to store user's choses and print it let them confirm
# json.dump()
