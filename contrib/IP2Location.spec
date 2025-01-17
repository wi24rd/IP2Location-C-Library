%define	version 8.4.0

Name:		IP2Location
Summary:	C library for mapping IP address to geolocation information
Version:	%{version}
Release:	8%{?dist}
License:	MIT
URL:		http://www.ip2location.com/
Source0:	https://github.com/chrislim2888/IP2Location-C-Library/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	libtool
BuildRequires:	perl(Math::BigInt)


%description
IP2Location C library enables the user to get the country, region, city,
coordinates, ZIP code, time zone, ISP, domain name, connection type,
area code, weather info, mobile carrier, elevation and usage type from any IP
address or hostname. This library has been optimized for speed and memory
utilization. The library contains API to query all IP2Location LITE and
commercial binary databases.

Users can download the latest LITE database from IP2Location web site using e.g.
the included downloader.


%package 	devel
Summary:	Static library and header files for the IP2Location library
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description 	devel
IP2Location C library enables the user to get the country, region, city,
coordinates, ZIP code, time zone, ISP, domain name, connection type,
area code, weather info, mobile carrier, elevation and usage type from any IP
address or hostname. This library has been optimized for speed and memory
utilization. The library contains API to query all IP2Location LITE and
commercial binary databases.

This package contains the development files for the IP2Location library.


%package 	data-sample
Summary:	Sample data files for the IP2Location library
Requires:	%{name} = %{version}-%{release}

%description 	data-sample
IP2Location C library enables the user to get the country, region, city,
coordinates, ZIP code, time zone, ISP, domain name, connection type,
area code, weather info, mobile carrier, elevation and usage type from any IP
address or hostname. This library has been optimized for speed and memory
utilization. The library contains API to query all IP2Location LITE and
commercial binary databases.

This package contains the sample data files for testing the library.

Latest lite databases can be downloaded from https://lite.ip2location.com


%prep
%setup -q -n IP2Location-C-Library-%{version}

# remove a warning option which break configure on older gcc versions
# (at least gcc version 4.1.2 20080704)
perl -pi -e 's/-Wno-unused-result//' configure.ac


%build
sh ./bootstrap
autoreconf -fiv

%configure --disable-static
%make_build COPTS="$RPM_OPT_FLAGS"

# convert CSV to BIN
make -C data convert


%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir}:$LD_LIBRARY_PATH make check


%install
%make_install

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

# tools
install -d %{buildroot}%{_datadir}/%{name}/tools
install -pm 0755 tools/download.pl %{buildroot}%{_datadir}/%{name}/tools

# database directory
install -d %{buildroot}%{_datadir}/%{name}/
# note: according to https://www.ip2location.com/development-libraries/ip2location/c
# IPv6 sample file has *.SAMPLE* while IPv4 has *-SAMPLE* in ZIP file
install -p data/IP-COUNTRY.BIN %{buildroot}%{_datadir}/%{name}/IP-COUNTRY-SAMPLE.BIN
install -p data/IPV6-COUNTRY.BIN %{buildroot}%{_datadir}/%{name}/IPV6-COUNTRY.SAMPLE.BIN


%files
%license COPYING LICENSE.TXT

%doc AUTHORS ChangeLog README.md NEWS

%{_libdir}/libIP2Location.so.1
%{_libdir}/libIP2Location.so.1.0.0

%{_datadir}/%{name}/tools/

%dir %{_datadir}/%{name}/


%files devel
%{_includedir}/IP2Loc*.h
%{_libdir}/libIP2Location.so

%doc Developers_Guide.txt


%files data-sample
%attr(644,-,-) %{_datadir}/%{name}/*.BIN


%changelog
* Thu May 20 2021 IP2Location <support@ip2location.com> - 8.4.0
- added supports for DB25 to display address type and category fields

* Mon Nov 09 2020 IP2Location <support@ip2location.com> - 8.3.1-1
- fixed version number

* Tue Nov 03 2020 IP2Location <support@ip2location.com> - 8.3.1
- included ip2location lookup

* Fri Oct 30 2020 IP2Location <support@ip2location.com> - 8.3.0
- added new interface "IP2Location_bin_version" to display BIN database version

* Thu Oct 01 2020 IP2Location <support@ip2location.com> - 8.2.0
- reverted changes based on 8.0.9

* Wed Sep 30 2020 IP2Location <support@ip2location.com> - 8.1.4
- restored internal variables

* Fri Sep 27 2020 IP2Location <support@ip2location.com> - 8.1.3
- restored functions renamed in 8.1.0.

* Fri Sep 25 2020 IP2Location <support@ip2location.com> - 8.1.2
- fixed version number in multiple places

* Fri Sep 25 2020 IP2Location <support@ip2location.com> - 8.1.1
- fixed "IP2Location_get_netspeed" function
- bumped up soname
- updated Developers_Guide.txt

* Thu Sep 24 2020 IP2Location <support@ip2location.com> - 8.1.0-1
- fixed version number and typo

* Thu Sep 24 2020 IP2Location <support@ip2location.com> - 8.1.0
- fixed memory leak issues

* Tue Sep 15 2020 Peter Bieringer <pb@bieringer.de> - 8.0.9-8
- new subpackage data-sample

* Tue Sep 08 2020 Peter Bieringer <pb@bieringer.de> - 8.0.9-6
- add missing BuildRequires perl(Math::BigInt)

* Fri Aug 28 2020 Peter Bieringer <pb@bieringer.de>
- fix spec file according to BZ#1873302

* Sat Oct  5 2019 Peter Bieringer <pb@bieringer.de> - 8.0.9-5
- update version to 8.0.9

* Sun Feb 26 2017 Peter Bieringer <pb@bieringer.de> - 8.0.4-5
- update to 8.0.4
- add some fixes related to move to github
- integrate download.pl into github tree

* Sun May 03 2015 Peter Bieringer <pb@bieringer.de> - 7.0.1-4
- add Developers_Guide.txt to doc/devel
- change group of base package to System Environment/Libraries
- add check/post/postuninstall section
- migrate some settings from http://www.ip2location.com/rpm/ip2location-c.spec

* Fri Apr 17 2015 Peter Bieringer <pb@bieringer.de> - 7.0.1-3
- update to 7.0.1
- add ip2location-downloader/download.pl

* Thu Apr 16 2015 Peter Bieringer <pb@bieringer.de>
- update to 7.0.0

* Sat Jan 24 2015 Peter Bieringer <pb@bieringer.de>
- run "make clean" before "make" cleanup i368 objects containend in source code

* Sun Jul 20 2014 Peter Bieringer <pb@bieringer.de>
- adjustments for 6.0.2

* Thu Aug 22 2013 Peter Bieringer <pb@bieringer.de>
- adjustments for 6.0.1, update license version
- some RPM fixes

* Sun May 15 2011 Oden Eriksson <oeriksson@mandriva.com> 4.0.2-1mdv2011.0
+ Revision: 674881
- import ip2location

* Sun May 15 2011 Oden Eriksson <oeriksson@mandriva.com> 4.0.2-1mdv2010.2
- initial Mandriva package
