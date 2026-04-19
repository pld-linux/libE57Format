#
# Conditional build:
%bcond_without	tests		# build without tests
#
Summary:	Library for reading & writing the E57 file format
Name:		libE57Format
Version:	3.3.0
Release:	1
License:	Boost Software License
Group:		Libraries
Source0:	https://github.com/asmaloney/libE57Format/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e0b5ca94917457bd61692d3e8c78fec9
Source1:	https://github.com/asmaloney/libE57Format-test-data/archive/main/libE57Format-test-data.tar.gz
# Source1-md5:	5e38e91a951c2afce5055f1f251fb5da
Patch0:		use-packaged-gtest.patch
Patch1:		numeric_limits.patch
URL:		https://github.com/asmaloney/libE57Format?tab=readme-ov-file
BuildRequires:	cmake
%if %{with tests}
BuildRequires:	gtest-devel
BuildRequires:	libasan-devel
BuildRequires:	libubsan-devel
%endif
BuildRequires:	xerces-c-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libE57Format is a C++ library which provides read & write support for
the ASTM-standard E57 file format on Linux, macOS, and Windows. E57
files store 3D point cloud data (produced by 3D imaging systems such
as laser scanners), attributes associated with 3D point data (color &
intensity), and 2D images (photos taken using a 3D imaging system).

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q -a1
%patch -P0 -p1
%patch -P1 -p1

%build
mkdir -p build
cd build
%cmake ../ \
%if %{with tests}
	-DE57_BUILD_TEST=ON \
	-DE57_TEST_DATA_PATH=libE57Format-test-data \
	-DUSE_PACKAGED_GTEST=ON
%else
	-DE57_BUILD_TEST=OFF
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%{_libdir}/%{name}.so.*.*.*
%ghost %{_libdir}/%{name}.so.3

%files devel
%defattr(644,root,root,755)
%doc CHANGELOG.md CONTRIBUTING.md
%{_libdir}/%{name}.so
%{_includedir}/E57Format
%{_libdir}/cmake/E57Format
