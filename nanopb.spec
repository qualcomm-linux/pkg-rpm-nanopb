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
BuildRequires:  python3-devel
BuildRequires:  python3-protobuf
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  protobuf-compiler
BuildRequires:  protobuf-devel

%description
Nanopb is a small code-size Protocol Buffers implementation.

%package devel
Summary:        Nanopb development headers
Requires:       %{name} = %{version}-%{release}

%description devel
Nanopb development headers and libraries.

%package generator
Summary:        Nanopb protoc plugin
Requires:       python3
Requires:       python3-protobuf

%description generator
Provides the protoc-gen-nanopb plugin.

%prep
%autosetup -n %{prj_name}-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

# Install generator plugin and scripts when they are not installed by CMake.
install -d %{buildroot}%{_bindir}
if [ -f generator/protoc-gen-nanopb ]; then
    install -m 0755 generator/protoc-gen-nanopb \
        %{buildroot}%{_bindir}/protoc-gen-nanopb
fi
if [ -f generator/nanopb_generator.py ] && \
   [ ! -e %{buildroot}%{_bindir}/nanopb_generator.py ]; then
    install -m 0755 generator/nanopb_generator.py \
        %{buildroot}%{_bindir}/nanopb_generator.py
fi
if [ -f generator/nanopb_generator ] && \
   [ ! -e %{buildroot}%{_bindir}/nanopb_generator ]; then
    install -m 0755 generator/nanopb_generator \
        %{buildroot}%{_bindir}/nanopb_generator
fi

# Create pkg-config file only if CMake did not generate one.
if [ ! -f %{buildroot}%{_libdir}/pkgconfig/nanopb.pc ]; then
    install -d %{buildroot}%{_libdir}/pkgconfig
    cat > %{buildroot}%{_libdir}/pkgconfig/nanopb.pc << PCEOF
prefix=/usr
exec_prefix=\${prefix}
libdir=\${exec_prefix}/%{_lib}
includedir=\${prefix}/include/nanopb

Name: nanopb
Description: Nanopb Protocol Buffers for Embedded Systems
Version: %{version}
Libs: -L\${libdir} -lprotobuf-nanopb
Cflags: -I\${includedir}
PCEOF
fi

# Do not package generated Python bytecode caches.
find %{buildroot}%{python3_sitelib} -type d -name __pycache__ \
    -prune -exec rm -rf {} + 2>/dev/null || :

%files
%license LICENSE.txt
%doc README.md CHANGELOG.txt
%{_libdir}/libprotobuf-nanopb.so.*

%files devel
%{_includedir}/nanopb/
%{_libdir}/libprotobuf-nanopb.so
%{_libdir}/libprotobuf-nanopb.a
%{_libdir}/pkgconfig/nanopb.pc
%{_libdir}/cmake/nanopb/

%files generator
%{_bindir}/protoc-gen-nanopb
%{_bindir}/nanopb_generator*
%{python3_sitelib}/nanopb/

%changelog
* Mon Sep 14 2026 mmritunj@qti.qualcomm.com - 0.4.9.1-1
- Initial RPM build
