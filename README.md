Introduction
============

About python-ipset
------------------

**ipset** is used to set up, maintain and inspect so called IP sets in the
Linux kernel. Depending on the type of the set, an IP set may store
IP(v4/v6) addresses, (TCP/UDP) port numbers, IP and MAC address pairs, IP
address and port number pairs, etc.

**iptables** matches and targets referring to sets create references, which
protect the given sets in the kernel. A set cannot be destroyed while there
is a single reference pointing to it.

`Python-ipset` provides a pythonesque wrapper via python bindings to
ipset under Linux. Interoperability with the many versions of the netfilter
protocol ipset has used is achieved via using the ipset C libraries
(libipset).
