%bcond_without check
%global crate zram-generator

Name:		rust-%{crate}
Version:	0.3.2
Release:	1
Summary:	Systemd unit generator for zram devices
Group:		System/Libraries
# Upstream license specification: MIT
License:	MIT
URL:		https://crates.io/crates/zram-generator
Source0:	%{crates_source}
ExclusiveArch:  %{rust_arches}
%if %{__cargo_skip_build}
BuildArch:      noarch
%endif
BuildRequires:  rust-packaging

%global _description %{expand:
This is a systemd unit generator that creates a unit file to create a
zram device. To activate, copy
/usr/share/doc/rust-zram-generator/zram-generator.conf.example to
/etc/systemd/zram-generator.conf and possibly edit to adjust the limits.}

%description %{_description}

%package -n %{crate}
Summary:	%{summary}

%description -n %{crate} %{_description}

%files -n %{crate}
%license LICENSE
%doc zram-generator.conf.example
%doc README.md TODO
%{_systemdgeneratordir}/zram-generator

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires
echo 'systemd-rpm-macros'

%build
%cargo_build

%install
%cargo_install

mkdir -p %{buildroot}%{_systemdgeneratordir}
mv -v %{buildroot}%{_bindir}/zram-generator %{buildroot}%{_systemdgeneratordir}/

%if %{with check}
%check
%cargo_test
%endif
