%undefine        _debugsource_packages
%global soc      sunxi64
Version:         6.18.6
Release:         2.%{soc}%{?dist}
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
