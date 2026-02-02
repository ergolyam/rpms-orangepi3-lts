%global commit db5e86200ae592c467c4cfa50ec0c66cbc40b158
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           uwe5622-firmware
Version:        1.0
Release:        1.git%{shortcommit}%{?dist}
Summary:        Unisoc UWE5622 (AW859A) Wi-Fi/Bluetooth firmware
License:        Unknown
URL:            https://github.com/orangepi-xunlong/firmware
Source0:        %{url}/archive/%{commit}/firmware-%{commit}.tar.gz
BuildArch:      noarch
AutoReqProv:    no

%description
Firmware for the Unisoc UWE5622 (AW859A) Wi-Fi/Bluetooth combo.
Packaged from the Orange Pi firmware repository.

%prep
%autosetup -n firmware-%{commit}

%install
install -Dm 0644 wcnmodem.bin %{buildroot}/usr/lib/firmware/wcnmodem.bin
install -Dm 0644 wifi_2355b001_1ant.ini %{buildroot}/usr/lib/firmware/wifi_2355b001_1ant.ini
install -Dm 0644 bt_configure_rf.ini %{buildroot}/usr/lib/firmware/bt_configure_rf.ini
install -Dm 0644 bt_configure_pskey.ini %{buildroot}/usr/lib/firmware/bt_configure_pskey.ini

%files
/usr/lib/firmware/wcnmodem.bin
/usr/lib/firmware/wifi_2355b001_1ant.ini
/usr/lib/firmware/bt_configure_pskey.ini
/usr/lib/firmware/bt_configure_rf.ini

%changelog
%autochangelog
