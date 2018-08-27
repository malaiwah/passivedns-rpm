%define logdir          /var/log
%define logrotatedir    /etc/logrotate.d
%define runtimedir      /var/run
%define initdir         /etc/init.d

Name: passivedns
Version: 1.2.1
Release: 1.20180703git945fcea.el5
Summary: A network sniffer that logs all DNS server replies for use in a passive DNS setup
License: GPLv2
Group: Monitoring
URL: https://github.com/gamelinux/passivedns
Source: %name-%version.tar.gz
Patch:  passivedns-syslog.patch
Packager: Fabian Dammekens <fabian@dammekens.be>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libpcap-devel ldns-devel perl-DateTime perl-DBI perl-Date-Simple openssl-devel

%description
A tool to collect DNS records passively to aid Incident handling, Network
Security Monitoring (NSM) and general digital forensics.

PassiveDNS sniffes traffic from an interface or reads a pcap-file and outputs
the DNS-server answers to a log file. PassiveDNS can cache/aggregate duplicate
DNS answers in-memory, limiting the amount of data in the logfile without
loosing the essens in the DNS answer.

%package daemon
Summary: Daemon for passive DNS
Group: Monitoring
Requires: %name = %version-%release

%description daemon
Daemon for %name

%package tools
Summary: Tools for passive DNS
Group: Monitoring

%description tools
A tools for work with %name data

%prep
%setup

%patch

%build
autoreconf --install
export CPPFLAGS='-I/usr/include/ldns'
./configure
make

%install
install -pD -m755 src/%name %buildroot%_sbindir/%name
install -pD -m755 tools/pdns2db.pl %buildroot%_bindir/pdns2db.pl
install -pD -m755 tools/search-pdns.pl %buildroot%_bindir/search-pdns.pl
mkdir -p %buildroot%{logdir}/%name
mkdir -p %buildroot%_sharedstatedir/%name
mkdir -p %buildroot%_sysconfdir/sysconfig
mkdir -p %buildroot%{runtimedir}/%name
mkdir -p %buildroot%{logrotatedir}
install -pD -m755 etc/init.d/passivedns-redhat %buildroot%{initdir}/%name
install -pD -m755 etc/sysconfig/passivedns-redhat %buildroot%_sysconfdir/sysconfig/%name
install -pD -m755 etc/logrotate.d/passivedns %buildroot%{logrotatedir}/%name

sed -i "s|^LOGFILE=|LOGFILE=%{logdir}/%name/%name.log|g" %buildroot%_sysconfdir/sysconfig/%name
sed -i "s|^/var/log/%name.log {|%{logdir}/%name/%name.log {|g" %buildroot%_sysconfdir/logrotate.d/%name
sed -i "s|^USER=|USER=passivedns|g" %buildroot%_sysconfdir/sysconfig/%name
sed -i "s|^GROUP=|GROUP=passivedns|g" %buildroot%_sysconfdir/sysconfig/%name
sed -i "s|^INTERFACE=|INTERFACE=eth0|g" %buildroot%_sysconfdir/sysconfig/%name
sed -i "s|^PIDFILE=|PIDFILE=%{runtimedir}/%name/%name.pid|g" %buildroot%_sysconfdir/sysconfig/%name

%pre
/usr/sbin/groupadd -r -f %name
/usr/sbin/useradd -r -g %name -d %_sharedstatedir/%name -s /dev/null -n -c "DNS network sniffer" %name >/dev/null 2>&1 ||:

%post daemon
/sbin/chkconfig %name off

%preun daemon
/sbin/service %name stop

%files
%doc README doc tools/README.skip_white_black-list.txt
%_sbindir/*
%dir %attr(0770,root,%name) %{logdir}/%name
%{logrotatedir}/%name

%files daemon
%dir %_sharedstatedir/%name
%dir %attr(775,root,%name) %{runtimedir}/%name
%config(noreplace) %_sysconfdir/sysconfig/%name
%{initdir}/*

%files tools
%_bindir/*.pl

%changelog
* Mon Aug 27 2018 Michel Belleau <michel.belleau@malaiwah.com> 1.2.1-1.20180703git945fcea
- Adjusted to be working on old ancient EL5 and bumped up passivedns version to latest 1.2.1
* Wed Oct 21 2015 Fabian Dammekens <fabian@dammekens.be> 1.2.0-3.20151019git3e0611d
- patch to send syslog messages to facility local6
* Wed Sep 23 2015 Fabian Dammekens <fabian@dammekens.be> 1.2.0-1.20150923gitdda831c
- bump to upstream release, built for RHEL
* Tue Mar 20 2012 Slava Dubrovskiy <dubrsl@altlinux.org> 0.3.3-alt1
- built for ALT Linux
