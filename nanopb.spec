%global prj_name    nanopb
%global debug_package %{nil}

Name:           nanopb
Version:        0.4.9.1
Release:        %autorelease
Summary:        Nanopb Protocol Buffers for Embedded Systems

License:        zlib
URL:            https://github.com/nanopb/nanopb
Source0:        %{url}/archive/%{version}/%{prj_name}-%{version}.tar.gz

ExclusiveArch:  %{arm64}

BuildRequires:  python3
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  protobuf-compiler
BuildRequires:  protobuf-devel

%description
Nanopb is a small code-size Protocol Buffers implementation.

%package devel
Summary:  Nanopb development headers
Requires: %{name} = %{version}-%{release}

%description devel
Nanopb development headers and libraries.

%package generator
Summary:  Nanopb protoc plugin
Requires: python3

%description generator
Provides the protoc-gen-nanopb plugin.

%prep
%autosetup -n nanopb

%build
cmake . -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_SHARED_LIBS=ON
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Install generator plugin
mkdir -p %{buildroot}/usr/bin
install -m 755 generator/protoc-gen-nanopb %{buildroot}/usr/bin/protoc-gen-nanopb

# Manually create pkg-config file
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/nanopb.pc << PCEOF
prefix=/usr
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib64
includedir=\${prefix}/include/nanopb

Name: nanopb
Description: Nanopb Protocol Buffers for Embedded Systems
Version: 0.4.9.1
Libs: -L\${libdir} -lprotobuf-nanopb
Cflags: -I\${includedir}
PCEOF

# ── Base runtime package ──────────────────────────────────────
%files
%{_libdir}/libprotobuf-nanopb.so.*

# ── Devel package ─────────────────────────────────────────────
%files devel
%{_includedir}/nanopb/
%{_libdir}/libprotobuf-nanopb.so
%{_libdir}/libprotobuf-nanopb.a
%{_libdir}/pkgconfig/nanopb.pc
%{_libdir}/cmake/nanopb/

# ── Generator package ─────────────────────────────────────────
%files generator
/usr/bin/protoc-gen-nanopb
/usr/bin/nanopb_generator
/usr/bin/nanopb_generator.py
/usr/lib/python3.12/site-packages/nanopb/

%changelog
* Mon Sep 14 2026 mmritunj@qti.qualcomm.com - 0.4.9.1-1
- Initial RPM build
