Name: kernel
ExclusiveArch: aarch64
Version: 6.17.6
Release: 1.sunxi64
Summary: AIO package for linux kernel, modules and headers for Orange PI 3 LTS (sunxi64).
Source1: https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
Source2: https://github.com/armbian/build/raw/7828980921716b46ba3e854ba64b2735325c2d04/config/kernel/linux-sunxi64-current.config
Patch1: https://lore.kernel.org/all/20250413134318.66681-2-jernej.skrabec@gmail.com/raw#/0002-sunxi-bindings.patch
Patch2: https://lore.kernel.org/all/20250413134318.66681-3-jernej.skrabec@gmail.com/raw#/0003-orangepi3-lts-dtb.patch
License: GPL

Provides: kernel = %{version}-%{release}
Provides: kernel-core = %{version}-%{release}
Provides: kernel-modules = %{version}-%{release}

BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: zstd
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex, gcc-c++
BuildRequires: rust, rust-src, bindgen, rustfmt, clippy
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: dwarves
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pyyaml
BuildRequires: glibc-static
BuildRequires: rsync
BuildRequires: opencsd-devel >= 1.0.0
BuildRequires: openssl-devel

Requires: dracut >= 027
Requires: bash
Requires: coreutils
Requires: systemd

%description
Mainline kernel for Orange PI 3 LTS (sunxi64).

%prep
tar -xf %{SOURCE1}
cd linux-%{version}
cp %{SOURCE2} .config
patch -p1 -i %{PATCH1}
patch -p1 -i %{PATCH2}

%build
cd linux-%{version}
make LOCALVERSION="-%{release}" olddefconfig
scripts/config --disable WERROR
make EXTRAVERSION="-%{release}" -j`nproc`

%install
cd linux-%{version}
kernel_version=$(make EXTRAVERSION="-%{release}" kernelrelease)

mkdir -p %{buildroot}/boot/
cp arch/arm64/boot/Image.gz %{buildroot}/boot/vmlinuz-$kernel_version
cp System.map %{buildroot}/boot/System.map-$kernel_version
cp .config %{buildroot}/boot/config-$kernel_version

make EXTRAVERSION="-%{release}" modules_install INSTALL_MOD_PATH=%{buildroot}/usr
cp arch/arm64/boot/dts/allwinner/sun50i-h6-orangepi-3-lts.dtb %{buildroot}/usr/lib/modules/$kernel_version/devicetree
ln -s ./devicetree %{buildroot}/usr/lib/modules/$kernel_version/dtb
cp arch/arm64/boot/Image.gz %{buildroot}/usr/lib/modules/$kernel_version/vmlinuz
make EXTRAVERSION="-%{release}" headers_install INSTALL_HDR_PATH=%{buildroot}/usr
rm %{buildroot}/usr/lib/modules/%{version}*/build

%files
/boot/System.map-%{version}*
/boot/config-%{version}*
/boot/vmlinuz-%{version}*
/usr/lib/modules/%{version}*

%posttrans
kernel-install add %{version}-%{release} /usr/lib/modules/%{version}-%{release}/vmlinuz

%postun
kernel-install remove %{version}-%{release} /usr/lib/modules/%{version}-%{release}/vmlinuz


%package core
License: GPL
Summary: AIO package for linux kernel, modules and headers for Orange PI 3 LTS (sunxi64).
Requires: kernel

%description core
Mainline kernel for Orange PI 3 LTS (sunxi64).

%files core


%package modules
License: GPL
Summary: AIO package for linux kernel, modules and headers for Orange PI 3 LTS (sunxi64).
Requires: kernel

%description modules
Mainline kernel for Orange PI 3 LTS (sunxi64).

%files modules


%package devel
License: GPL
Summary: AIO package for linux kernel, modules and headers for Orange PI 3 LTS (sunxi64).
Requires: kernel-headers

%description devel
Mainline kernel header for Orange PI 3 LTS (sunxi64).

%files devel


%package headers
License: GPL
Summary: AIO package for linux kernel, modules and headers for Orange PI 3 LTS (sunxi64).
Provides: kernel-devel = %{version}-%{release}

%description headers
Mainline kernel headers for Orange PI 3 LTS (sunxi64).

%files headers
/usr/include


%package devel-matched
License: GPL
Summary: AIO package for linux kernel, modules and headers for Orange PI 3 LTS (sunxi64).
Requires: kernel-devel
Requires: kernel-core

%description devel-matched
Mainline kernel headers for Orange PI 3 LTS (sunxi64).

%files devel-matched

