import os
import json
import time


class Arch_further_installer:
    def __init__(self) -> None:
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
        time.sleep(5)
        os.system("clear")

    def add_repo(self):
        CN_repo_list = {
            "USTC": """[archlinuxcn]\nServer = https://mirrors.ustc.edu.cn/archlinuxcn/$arch""",
            "Tsinghua": """[archlinuxcn]\nServer = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch\n""",
        }
        print(CN_repo_list.keys())
        confirm_CN_repo = input(
            "Input your CN repo provider(They provide same contents, input the SAME of printed)"
        )
        confirm_enable_32 = input("Do you want to enable 32-bit repo? y/n: ")
        with open("/etc/pacman.conf", "a") as pacman_config:
            pacman_config.write(CN_repo_list[confirm_CN_repo])
            if confirm_enable_32 == "y":
                pacman_config.write(
                    """\n\n[multilib]\nInclude = /etc/pacman.d/mirrorlist\n"""
                )

    def sync_data(self):
        # Update database
        os.system("pacman -Sy")
        # Install software
        packages = input(
            "Input your package name to install, CN repo and official repo ONLY, use `space` to split: "
        )
        os.system(f"pacman -S archlinuxcn-keyring archlinux-keyring {packages}")

    # Set hostname
    def set_hostname(self):
        global hostname
        hostname = input("Input your hostname:")
        with open("/etc/hostname", "w") as hostname_file:
            hostname_file.write(hostname)

    # Set host
    def set_host(self):
        with open("/etc/hosts", "w") as hosts_file:
            hosts_file.write(
                f"""127.0.0.1   localhost\n::1         localhost\n127.0.1.1   myarch.localdomain {hostname}"""
            )

    # Set local time to Asia/Shanghai
    def set_time(self):
        os.system("ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime")
        os.system("hwclock --systohc")

    # Locale
    def genarate_locale(self):
        with open("/etc/locale.gen", "a") as locale_file:
            locale_file.write("en_US.UTF-8")
            locale_file.write("zh_CN.UTF-8")
        os.system("locale-gen")
        os.system("echo 'LANG=en_US.UTF-8'  > /etc/locale.conf")

    # Set password
    def set_root_passwd(self):
        print("Input your root password")
        os.system("passwd root")

    # Create normal user
    def create_normal_user(self):
        normal_user_name = input("Input your normal username:")
        os.system("chsh -l")
        shell = input("Input the path of shell for user use: ")
        os.system(f"useradd -m -G wheel -s {shell} {normal_user_name}")
        os.system(f"passwd {normal_user_name}")

    # Bootloader
    def install_bootloader(self):
        confirm = input(
            "WARNING: use `grub` as default, if you want to use other bootloader, please input `o`: "
        )
        if confirm == "o":
            package = input("Input your bootloader package name: ")
            os.system(f"pacman -S {package}")
            print("Now you need to configure it manually")
        else:
            os.system("pacman -S grub grub-btrfs efibootmgr")
            os.system(
                "grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=ARCH"
            )
            print("There is something you need to visit: http://fars.ee/yGQq")
            os.system("grub-mkconfig -o /boot/grub/grub.cfg")


installer = Arch_further_installer()
installer.add_repo()
installer.change_mirror()
installer.sync_data()
installer.genarate_locale()
installer.set_host()
installer.set_hostname()
installer.set_root_passwd()
installer.set_time()
installer.create_normal_user()
installer.install_bootloader()
