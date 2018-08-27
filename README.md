# passivedns-rpm
This repository contains a basic SPEC file required to build an rpm of
[Gamelinux PassiveDNS](https://github.com/gamelinux/passivedns)

```
#
#  ______                                           ____   __  __  _____
# |  __  |                         @               |    \ |  \ | ||  ___| (TM)
# | _____|.------. .-----. .-----. _ -. .-.------. | |\  ||   \| ||___  |
# |  |    |  __  ||__  --'|__  --'| |\ Y /| _--__|_| |/  ||      || \_| |
# |__|    |____|_||______||______||_| \_/ |_______/|____/ |__|\__||_____|
#
#
```

A tool to collect DNS records passively to aid Incident handling, Network
Security Monitoring (NSM) and general digital forensics.

PassiveDNS sniffs traffic from an interface or reads a pcap-file and outputs
the DNS-server answers to a log file. PassiveDNS can cache/aggregate duplicate
DNS answers in-memory, limiting the amount of data in the logfile without
losing the essense in the DNS answer.

## Download SOURCE
```
wget "https://github.com/gamelinux/passivedns/archive/1.2.1.tar.gz" -O passivedns-1.2.1.tar.gz
```
## Build RPM
```
export rhel=el6
sudo yum-builddep -y SPECS/passivedns-${rhel}.spec
spectool -g -R SPECS/passivedns-${rhel}.spec
rpmbuild -ba -vv SPECS/passivedns-${rhel}.spec
```
## Alternative to download build dependencies
```
yum install -y libpcap-devel ldns-devel perl-DateTime perl-DBI perl-Date-Simple openssl-devel
```

Notice: a patch has been added to this SPEC which makes passivedns send it's logs to syslog via the local6 facility, instead of the local7 facility.

### TODO
Create systemd compatible service script

## References
Article: https://www.dammekens.be/2015/10/21/gamelinux-passivedns-rpm/
