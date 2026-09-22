%global prj_name    nanopb
%global debug_package %{nil}

Name:           nanopb
Version:        0.4.9.1
Release:        2%{?dist}
Summary:        A small code-size Protocol Buffers implementation in ansi C
License:        Zlib
URL:            https://github.com/nanopb/nanopb
Source0:        %{url}/archive/%{version}/%{prj_name}-%{version}.tar.gz
ExclusiveArch:  %{arm64}

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-compiler
BuildRequires:  python3-devel
BuildRequires:  python3-protobuf

%description
Nanopb is a small code-size Protocol Buffers implementation in ansi C. It is
especially suitable for use in microcontrollers, but fits any memory restricted
system.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package generator
Summary:        Nanopb protoc plugin
Requires:       python3
Requires:       python3-protobuf

%description generator
Provides the protoc-gen-nanopb plugin.

%prep
%autosetup -n %{prj_name}-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DBUILD_STATIC_LIBS=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE.txt
%doc README.md CHANGELOG.txt
%{_libdir}/libprotobuf-nanopb.so.0

%files devel
%{_includedir}/nanopb/
%{_libdir}/libprotobuf-nanopb.so
%{_libdir}/cmake/nanopb/

%files generator
%{_bindir}/protoc-gen-nanopb
%{_bindir}/nanopb_generator*
%{python3_sitelib}/nanopb/

%changelog
* Mon Sep 14 2026 Mritunjoy Das <mmritunj@qti.qualcomm.com> - 0.4.9.1-2
- Initial RPM build for open source nanopb library
