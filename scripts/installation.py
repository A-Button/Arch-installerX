import os


class Arch_installer:
    def __init__(self, partitions, system_packages, optional_mount_partition) -> None:
        # self.mirror = mirror
        self.partitions = partitions
        self.system_packages = system_packages
        self.optional_mount_partition = optional_mount_partition
        pass

    def change_mirror(self):
        mirros_list = {
            "TsingHua": "Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch",
            "USTC": "Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch",
            "LZU": "Server = https://mirrors.lzu.edu.cn/archlinux/$repo/os/$arch",
            "HuaWei_Cloud": "Server = https://mirrors.huaweicloud.com/archlinux/$repo/os/$arch",
            "Ali_Cloud": "Server = http://mirrors.aliyun.com/archlinux/$repo/os/$arch",
        }
        for key in mirros_list.keys():
            print(key)
        mirror = input(
            "Choose one mirror provider above(Name should be the SAME as printed, upcase), if you want to use other, please input `o`: "
        )
        if mirror == "o":
            print(
                "The mirror url form is `Server = https://<mirror_domain>/archlinux/$repo/os/$arch`"
            )
            mirror = input("Now please input the mirror url: ")
        elif mirror not in mirros_list.keys():
            print(
                "Please input the correct name(Name should be the SAME as printed, upcase)"
            )
            mirror = input(
                "Choose one mirror provider above(Name should be the SAME as printed, upcase), if you want to use other, please input `o`: "
            )
            mirror = mirros_list[mirror]
        elif mirror in mirros_list.keys():
            mirror = mirros_list[mirror]
        # os.system('cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.back')
        # with open('/etc/pacman.d/mirrorlist', 'w') as mirror_file:
        os.system("cp /home/Spark/mirrorlist /home/Spark/mirrorlist.back")
        with open("/home/Spark/mirrorlist", "w") as mirror_file:
            mirror_file.write(mirror)


installer = Arch_installer(
    input("partitions"),
    input("system_packages"),
    input("optional_mount_partition"),
)
installer.change_mirror()
