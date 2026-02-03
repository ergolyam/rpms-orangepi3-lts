%global armbian_build_commit 6f022174747f14f1b022f0eb707ff35cf1f5133c
%global shortcommit %(c=%{armbian_build_commit}; echo ${c:0:7})

Name:           hciattach-opi
Version:        1.0
Release:        1.git%{shortcommit}%{?dist}
Summary:        hciattach_opi helper for UWE5622 Bluetooth
License:        GPL-2.0-only
URL:            https://github.com/armbian/build
Source0:        %{url}/raw/%{armbian_build_commit}/packages/blobs/bt/hciattach/hciattach_opi_arm64_upstream
BuildArch:      aarch64
AutoReqProv:    no

%description
ARM64 hciattach_opi helper used by sprd-bluetooth for UWE5622 Bluetooth.

%install
install -Dm 0755 %{SOURCE0} %{buildroot}/usr/bin/hciattach_opi

%files
/usr/bin/hciattach_opi

%changelog
%autochangelog
