#!/usr/bin/env bash
set -euo pipefail

image="/usr/lib/u-boot/orangepi3-lts/u-boot-sunxi-with-spl.bin"
device="${UBOOT_INSTALL_DEVICE:-${1:-}}"

usage() {
    cat <<'USAGE'
Usage: u-boot-install-orangepi3-lts.sh [block-device]

If no block device is provided, the script attempts to detect the root disk.
Optional environment overrides:
  UBOOT_INSTALL_DEVICE  Explicit block device to write to
  UBOOT_DD_BS          dd block size (default: 1024)
  UBOOT_DD_SEEK        dd seek blocks (default: 8)
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
    usage
    exit 0
fi

if [ -z "$device" ]; then
    root_src="$(findmnt -nro SOURCE --target /)"
    root_dev="${root_src%%[*}"
    parent="$(lsblk -nro PKNAME "$root_dev" | head -n1)"
    if [ -n "$parent" ]; then
        device="/dev/$parent"
    else
        device="$root_dev"
    fi
fi

if [ -z "$device" ] || [ ! -b "$device" ]; then
    echo "Block device not found: $device" >&2
    exit 1
fi

if [ ! -f "$image" ]; then
    echo "U-Boot image not found: $image" >&2
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
    echo "Run as root to install U-Boot" >&2
    exit 1
fi

bs="${UBOOT_DD_BS:-1024}"
seek="${UBOOT_DD_SEEK:-8}"

echo "Writing $image to $device (bs=$bs seek=$seek)"
dd if="$image" of="$device" bs="$bs" seek="$seek" conv=fsync,notrunc status=progress
