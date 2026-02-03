%undefine        _debugsource_packages
%global soc      sunxi64
Version:         6.18.6
Release:         4.%{soc}%{?dist}
ExclusiveArch:   aarch64
Name:            kernel
Summary:         mainline kernel for %{soc}
License:         GPLv2
URL:             https://cdn.kernel.org/pub/linux/kernel
Source0:         %{url}/v6.x/linux-%{version}.tar.xz
Source1:         https://github.com/armbian/build/raw/7828980921716b46ba3e854ba64b2735325c2d04/config/kernel/linux-%{soc}-current.config
Source2:         armbian.config
Source3:         extra-%{soc}.config

Patch1:          https://lore.kernel.org/all/20250413134318.66681-2-jernej.skrabec@gmail.com/raw#/0002-sunxi-bindings.patch
Patch2:          https://lore.kernel.org/all/20250413134318.66681-3-jernej.skrabec@gmail.com/raw#/0003-orangepi3-lts-dtb.patch
Patch3:          https://github.com/armbian/build/raw/main/patch/kernel/archive/sunxi-6.18/patches.megous/modem-6.18/0001-misc-modem-power-Power-manager-for-modems.patch
Patch4:          https://github.com/armbian/build/raw/main/patch/kernel/archive/sunxi-6.18/patches.armbian/drv-misc-sunxi-add-addr-mgt-driver-uwe5622.patch
Patch5:          https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-allwinner-v6.3.patch
Patch6:          https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-allwinner-bugfix-v6.3.patch
Patch7:          https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-allwinner-v6.3-compilation-fix.patch
Patch8:          https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-v6.4-post.patch
Patch9:          https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-warnings.patch
Patch10:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-park-link-v6.1-post.patch
Patch11:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-v6.1.patch
Patch12:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-v6.6-fix-tty-sdio.patch
Patch13:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-fix-setting-mac-address-for-netdev.patch
Patch14:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/wireless-uwe5622-Fix-compilation-with-6.7-kernel.patch
Patch15:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/wireless-uwe5622-reduce-system-load.patch
Patch16:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-v6.9.patch
Patch17:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-v6.11.patch
Patch18:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-fix-spanning-writes.patch
Patch19:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-fix-timer-api-changes-for-6.15-only-sunxi.patch
Patch20:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-v6.16.patch
Patch21:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-v6.17.patch
Patch22:         https://github.com/armbian/build/raw/main/patch/misc/wireless-uwe5622/uwe5622-v6.18.patch

Provides:        kernel               = %{version}-%{release}
Provides:        kernel-core          = %{version}-%{release}
Provides:        kernel-devel         = %{version}-%{release}
Provides:        kernel-headers       = %{version}-%{release}
Provides:        kernel-modules       = %{version}-%{release}
Provides:        kernel-modules-core  = %{version}-%{release}

BuildRequires:   bc bison dwarves diffutils elfutils-devel findutils gcc gcc-c++ git-core hmaccalc hostname make openssl-devel perl-interpreter rsync tar which flex bzip2 xz zstd python3 python3-devel python3-pyyaml rust rust-src bindgen rustfmt clippy opencsd-devel net-tools

%global uname_r %{version}-%{release}.%{_target_cpu}

%description
%{summary}

%prep
%autosetup -n linux-%{version} -N
./scripts/kconfig/merge_config.sh -O . %{SOURCE1} %{SOURCE2} %{SOURCE3}
patch -p1 -i %{PATCH1}
patch -p1 -i %{PATCH2}
patch -p1 -i %{PATCH3}
patch -p1 -i %{PATCH4}
patch -p1 -i %{PATCH5}
patch -p1 -i %{PATCH6}
patch -p1 -i %{PATCH7}
patch -p1 -i %{PATCH8}
patch -p1 -i %{PATCH9}
patch -p1 -i %{PATCH10}
patch -p1 -i %{PATCH11}
patch -p1 -i %{PATCH12}
patch -p1 -i %{PATCH13}
patch -p1 -i %{PATCH14}
patch -p1 -i %{PATCH15}
patch -p1 -i %{PATCH16}
patch -p1 -i %{PATCH17}
patch -p1 -i %{PATCH18}
patch -p1 -i %{PATCH19}
patch -p1 -i %{PATCH20}
patch -p1 -i %{PATCH21}
patch -p1 -i %{PATCH22}
sed -i '/^CONFIG_LOCALVERSION=/d' .config

%build
make olddefconfig
make EXTRAVERSION="-%{release}.%{_target_cpu}" LOCALVERSION= -j%{?_smp_build_ncpus} Image modules dtbs

%install
make EXTRAVERSION="-%{release}.%{_target_cpu}" LOCALVERSION= INSTALL_MOD_PATH=%{buildroot}/usr INSTALL_HDR_PATH=%{buildroot}/usr modules_install headers_install
install -Dm644 arch/arm64/boot/dts/allwinner/sun50i-h6-orangepi-3-lts.dtb %{buildroot}/usr/lib/modules/%{uname_r}/devicetree
install -Dm644 arch/arm64/boot/Image %{buildroot}/usr/lib/modules/%{uname_r}/vmlinuz
install -Dm644 System.map            %{buildroot}/usr/lib/modules/%{uname_r}/System.map
install -Dm644 .config               %{buildroot}/usr/lib/modules/%{uname_r}/config
install -d %{buildroot}/usr/lib/kernel
install -d %{buildroot}/usr/lib/ostree-boot

%files
/usr/include
/usr/lib/modules/%{uname_r}

%posttrans
set -e
depmod -a %{uname_r}
dracut /usr/lib/modules/%{uname_r}/initramfs.img %{uname_r}
kernel-install add %{uname_r} /usr/lib/modules/%{uname_r}/vmlinuz /usr/lib/modules/%{uname_r}/initramfs.img

%changelog
%autochangelog
