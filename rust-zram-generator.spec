%bcond_with check
%global crate zram-generator

Name:		rust-%{crate}
Version:	1.1.2
Release:	2
Summary:	Systemd unit generator for zram devices
Group:		System/Libraries
# Upstream license specification: MIT
License:	MIT
URL:		https://crates.io/crates/zram-generator
Source0:	https://github.com/systemd/zram-generator/archive/refs/tags/%{crate}-%{version}.tar.gz
Source1:	zram-generator.conf
ExclusiveArch:	%{rust_arches}
%if %{__cargo_skip_build}
BuildArch:	noarch
%endif
BuildRequires:	rust-packaging
BuildRequires:	systemd-rpm-macros

%global _description %{expand:
This is a systemd unit generator that creates a unit file to create a
zram device. To activate, copy
/usr/share/doc/rust-zram-generator/zram-generator.conf.example to
/etc/systemd/zram-generator.conf and possibly edit to adjust the limits.}

%description %{_description}

%package -n %{crate}
Summary:	%{summary}
Recommends:	%{_bindir}/zramctl

%description -n %{crate} %{_description}

%files -n %{crate}
%license LICENSE
%doc zram-generator.conf.example
%doc README.md
%{_systemd_util_dir}/zram-generator.conf
%{_systemdgeneratordir}/zram-generator
%{_unitdir}/systemd-zram-setup@.service

%package devel
Summary:	%{summary}
BuildArch:	noarch

%description devel
This package contains library source intended for building other packages
which use "%{crate}" crate.

%files devel
%license LICENSE
%doc README.md
%{cargo_registry}/%{crate}-%{version_no_tilde}/

%package -n %{name}+default-devel
Summary:	%{summary}
BuildArch:	noarch

%description -n %{name}+default-devel
This package contains library source intended for building other packages
which use "default" feature of "%{crate}" crate.

%files -n %{name}+default-devel
%ghost %{cargo_registry}/%{crate}-%{version_no_tilde}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
cp -a %{S:1} .
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires
echo 'make'
echo 'ronn'
echo 'systemd-rpm-macros'

%build
export SYSTEMD_UTIL_DIR=%{_systemd_util_dir}
export LC_ALL=C.UTF-8
%cargo_build
%make_build SYSTEMD_SYSTEM_UNIT_DIR=%{_unitdir} SYSTEMD_SYSTEM_GENERATOR_DIR=%{_systemdgeneratordir} \
  systemd-service NOMAN=1

%install
export SYSTEMD_UTIL_DIR=%{_systemd_util_dir}
export SYSTEMD_SYSTEM_GENERATOR_DIR=%{_systemdgeneratordir}
%cargo_install

rm %{buildroot}%{_bindir}/zram-generator
%make_install SYSTEMD_SYSTEM_UNIT_DIR=%{_unitdir} SYSTEMD_SYSTEM_GENERATOR_DIR=%{_systemdgeneratordir} NOBUILD=1 NOMAN=1
install -Dpm0644 -t %{buildroot}%{_systemd_util_dir} %{SOURCE1}

%if %{with check}
%check
export SYSTEMD_UTIL_DIR=%{_systemd_util_dir}
%cargo_test
%endif
