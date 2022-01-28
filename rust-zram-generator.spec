%bcond_with check
%global crate zram-generator

Name:		rust-%{crate}
Version:	1.1.1
Release:	1
Summary:	Systemd unit generator for zram devices
Group:		System/Libraries
# Upstream license specification: MIT
License:	MIT
URL:		https://crates.io/crates/zram-generator
Source0:	https://github.com/systemd/zram-generator/archive/refs/tags/v%{version}.tar.gz
Source1:        zram-generator.conf
ExclusiveArch:  %{rust_arches}
%if %{__cargo_skip_build}
BuildArch:      noarch
%endif
BuildRequires:  rust-packaging
BuildRequires:  systemd-rpm-macros

%global _description %{expand:
This is a systemd unit generator that creates a unit file to create a
zram device. To activate, copy
/usr/share/doc/rust-zram-generator/zram-generator.conf.example to
/etc/systemd/zram-generator.conf and possibly edit to adjust the limits.}

%description %{_description}

%package -n %{crate}
Summary:	%{summary}
Recommends:     /sbin/zramctl

%description -n %{crate} %{_description}

%files -n %{crate}
%license LICENSE
%doc zram-generator.conf.example
%doc README.md
%{_prefix}/lib/systemd/zram-generator.conf
%{_systemdgeneratordir}/zram-generator
%{_unitdir}/systemd-zram-setup@.service

%package        devel
Summary:        %{summary}
BuildArch:      noarch
	
%description    devel %{_description}
This package contains library source intended for building other packages
which use "%{crate}" crate.

%files          devel
%license LICENSE
%doc README.md
%{cargo_registry}/%{crate}-%{version_no_tilde}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}
This package contains library source intended for building other packages
which use "default" feature of "%{crate}" crate.

%files       -n %{name}+default-devel
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
%cargo_build
make systemd-service SYSTEMD_SYSTEM_UNIT_DIR=%{_unitdir} SYSTEMD_SYSTEM_GENERATOR_DIR=%{_systemdgeneratordir}

%install
export SYSTEMD_UTIL_DIR=%{_systemd_util_dir}
%cargo_install
	
mkdir -p %{buildroot}%{_systemdgeneratordir}
mv -v %{buildroot}%{_bindir}/zram-generator %{buildroot}%{_systemdgeneratordir}/
install -Dpm0644 -t %{buildroot}%{_unitdir} units/systemd-zram-setup@.service
install -Dpm0644 -t %{buildroot}%{_prefix}/lib/systemd %{SOURCE1}

%if %{with check}
%check
export SYSTEMD_UTIL_DIR=%{_systemd_util_dir}
%cargo_test
%endif
