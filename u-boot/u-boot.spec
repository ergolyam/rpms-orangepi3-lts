%undefine _debugsource_packages
%global tfa_version 2.14.0
%global plat sun50i_h6
%global uboot_defconfig orangepi_3_defconfig
%global cross_compile %{nil}
%global target_cc gcc
%if "%{_build_cpu}" != "%{_target_cpu}"
%global cross_compile aarch64-linux-gnu-
%global target_cc %{cross_compile}gcc
%endif

Name:           u-boot
Version:        2026.01
Release:        1.%{plat}%{?dist}
Summary:        U-Boot for Orange Pi 3 LTS
License:        GPL-2.0-or-later
URL:            https://www.denx.de/wiki/U-Boot
Source0:        https://ftp.denx.de/pub/u-boot/u-boot-%{version}.tar.bz2
Source1:        https://github.com/ARM-software/arm-trusted-firmware/archive/refs/tags/v%{tfa_version}.tar.gz
Source2:        u-boot-install-orangepi3-lts.sh
ExclusiveArch:  aarch64
AutoReqProv:    no
Requires:       bash coreutils util-linux
BuildRequires:  bc bison flex gcc make openssl-devel python3 python3-devel python3-pyyaml python3-setuptools swig
BuildRequires:  binutils-aarch64-linux-gnu gcc-aarch64-linux-gnu

%description
U-Boot bootloader for the Orange Pi 3 LTS (Allwinner H6).

%prep
%autosetup -n u-boot-%{version} -a1

%build
pushd arm-trusted-firmware-%{tfa_version}
make -j%{?_smp_build_ncpus} PLAT=%{plat} CC=%{target_cc} CROSS_COMPILE=%{cross_compile} CFLAGS= LDFLAGS=
popd

make %{uboot_defconfig} CC=%{target_cc} CROSS_COMPILE=%{cross_compile} HOSTCC=gcc HOSTCFLAGS= HOSTLDFLAGS= CFLAGS= LDFLAGS=
./scripts/config --disable TOOLS_KWBIMAGE --disable TOOLS_LIBCRYPTO --disable TOOLS_MKEFICAPSULE
make -j%{?_smp_build_ncpus} BL31=arm-trusted-firmware-%{tfa_version}/build/%{plat}/release/bl31.bin CC=%{target_cc} CROSS_COMPILE=%{cross_compile} HOSTCC=gcc HOSTCFLAGS= HOSTLDFLAGS= CFLAGS= LDFLAGS=

%install
install -Dm 0644 u-boot-sunxi-with-spl.bin %{buildroot}/usr/lib/u-boot/orangepi3-lts/u-boot-sunxi-with-spl.bin
install -Dm 0755 %{SOURCE2} %{buildroot}/usr/sbin/orangepi3-lts-install-uboot

%post
if [ "${UBOOT_INSTALL_SKIP:-0}" != "1" ]; then
    /usr/sbin/orangepi3-lts-install-uboot
fi

%files
%license Licenses/README
%doc README
/usr/lib/u-boot/orangepi3-lts/u-boot-sunxi-with-spl.bin
/usr/sbin/orangepi3-lts-install-uboot

%changelog
%autochangelog
