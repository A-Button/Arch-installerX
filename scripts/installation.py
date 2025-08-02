import os


class Arch_installer:
    def __init__(self, optional_mount_partition) -> None:
        # self.mirror = mirror
        self.system_packages = []
        self.optional_mount_partition = optional_mount_partition
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
            confirm_subvolume_name = input("Do you want to set your subvolume name? y/n ")
            if confirm_subvolume_name == 'y':
                subvolume_name_for_root = input("Input your subvolume name for *root* partition: ")
                subvolume_name_for_home = input("Input your subvolume name for *home* partition: ")
                os.system(f"btrfs subvolume create /mnt/{subvolume_name_for_root}")
                os.system(f"btrfs subvolume create /mnt/{subvolume_name_for_home}")
            else:
                os.system("btrfs subvolume create /mnt/@")
                os.system("btrfs subvolume create /mnt/@home")
            os.system("umount /mnt")
        else:
            pass

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
        os.system("clear")


installer = Arch_installer(
    # input("partitions"),
    # input("system_packages"),
    input("optional_mount_partition"),
)
installer.ask_partition_name(
    boot_partition=input("Input your boot partition:"),
    root_partition=input("Input your root partition:"),
    swap=input("Input your swap partition:"),
)
installer.change_mirror()
