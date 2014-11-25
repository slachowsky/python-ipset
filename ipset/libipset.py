import ctypes as ct

__all__ = ["Session"]

_libipset = ct.CDLL("libipset.so.3")
#_libipset = ct.CDLL("/home/stephan/repos/ipset/lib/.libs/libipset.so.3.6.0")

# Constants for ipset_session_output
IPSET_LIST_NONE = 0
IPSET_LIST_PLAIN = 1
IPSET_LIST_SAVE = 2
IPSET_LIST_XML = 3

# Constants for data options
# Common ones
IPSET_SETNAME = 1
IPSET_OPT_TYPENAME = 2
IPSET_OPT_FAMILY = 3
# CADT options
IPSET_OPT_IP = 4
IPSET_OPT_IP_FROM = IPSET_OPT_IP
IPSET_OPT_IP_TO = 5
IPSET_OPT_CIDR = 6
IPSET_OPT_PORT = 7
IPSET_OPT_PORT_FROM = IPSET_OPT_PORT
IPSET_OPT_PORT_TO = 8
IPSET_OPT_TIMEOUT = 9
# Create-specific options
IPSET_OPT_GC = 10
IPSET_OPT_HASHSIZE = 11
IPSET_OPT_MAXELEM = 12
IPSET_OPT_NETMASK = 13
IPSET_OPT_PROBES = 14
IPSET_OPT_RESIZE = 15
IPSET_OPT_SIZE = 16
# Create-specific options filled out by the kernel
IPSET_OPT_ELEMENTS = 17
IPSET_OPT_REFERENCES = 18
IPSET_OPT_MEMSIZE = 19
# ADT-specific options
IPSET_OPT_ETHER = 20
IPSET_OPT_NAME = 21
IPSET_OPT_NAMEREF = 22
IPSET_OPT_IP2 = 23
IPSET_OPT_CIDR2 = 24
IPSET_OPT_IP2_TO = 25
IPSET_OPT_PROTO = 26
IPSET_OPT_IFACE = 27
# Swap/rename to
IPSET_OPT_SETNAME2 = 28
# Flags
IPSET_OPT_EXIST = 29
IPSET_OPT_BEFORE = 30
IPSET_OPT_PHYSDEV = 31
IPSET_OPT_NOMATCH = 32
IPSET_OPT_COUNTERS = 33
IPSET_OPT_PACKETS = 34
IPSET_OPT_BYTES = 35
IPSET_OPT_CREATE_COMMENT = 36
IPSET_OPT_ADT_COMMENT = 37

# Message types and commands
IPSET_CMD_PROTOCOL = 1  # Return protocol version
IPSET_CMD_CREATE = 2    # Create a new (empty) set
IPSET_CMD_DESTROY = 3   # Destroy a (empty) set
IPSET_CMD_FLUSH = 4     # Remove all elements from a set
IPSET_CMD_RENAME = 5    # Rename a set
IPSET_CMD_SWAP = 6      # Swap two sets
IPSET_CMD_LIST = 7      # List sets
IPSET_CMD_SAVE = 8      # Save sets
IPSET_CMD_ADD = 9       # Add an element to a set
IPSET_CMD_DEL = 10      # Delete an element from a set
IPSET_CMD_TEST = 11     # Test an element in a set
IPSET_CMD_HEADER = 12   # Get set header data only
IPSET_CMD_TYPE = 13     # Get set type

class ipset(object):
    """This class contains the libipset API calls."""

    load_types = _libipset.ipset_load_types
    load_types.restype = None
    load_types.argstype = []
    
    session_init = _libipset.ipset_session_init
    session_init.restype = ct.POINTER(ct.c_int)
    session_init.argstype = [ct.c_void_p]
    
    session_outfn = _libipset.ipset_session_outfn
    session_outfn.restype = ct.c_int
    session_outfn.argstype = [ct.c_void_p]
    
    session_output = _libipset.ipset_session_output
    session_output.restype = ct.c_int
    session_output.argstype = [ct.c_void_p, ct.c_uint32]
    
    cmd = _libipset.ipset_cmd
    cmd.restype = ct.c_int
    cmd.argstype = [ct.POINTER(ct.c_int), ct.c_uint32, ct.c_uint32]

    type_get = _libipset.ipset_type_get
    type_get.restype = ct.c_void_p
    type_get.argstype = [ct.POINTER(ct.c_int), ct.c_uint32]
    
    parse_setname = _libipset.ipset_parse_setname
    parse_setname.restype = ct.c_int
    parse_setname.argstype = [ct.POINTER(ct.c_int), ct.c_uint32, ct.c_char_p]
    
    parse_typename = _libipset.ipset_parse_typename
    parse_typename.restype = ct.c_int
    parse_typename.argstype = [ct.POINTER(ct.c_int), ct.c_uint32, ct.c_char_p]

    parse_elem = _libipset.ipset_parse_elem
    parse_elem.restype = ct.c_int
    parse_elem.argstype = [ct.POINTER(ct.c_int), ct.c_uint32, ct.c_char_p]

ipset.load_types()

OUTFN = ct.CFUNCTYPE(None, ct.c_char_p, ct.c_char_p)

class ResultAccumulator(object):
    def __init__(self):
        self.result = ''
    def __call__(self, a, b):
        self.result += b

import xml.etree.ElementTree as ET

class Session(object):
    def __init__(self):
        self._session = ipset.session_init(0)
        ipset.session_outfn(self._session, 0)
        ipset.session_output(self._session, IPSET_LIST_XML)

    def add(self, name, value):
        ipset.parse_setname(self._session, IPSET_SETNAME, name)
        ipset.type_get(self._session, IPSET_CMD_ADD)
        ipset.parse_elem(self._session, 1, value)
        return ipset.cmd(self._session, IPSET_CMD_ADD, 0)

    def test(self, name, value):
        ipset.parse_setname(self._session, IPSET_SETNAME, name)
        ipset.type_get(self._session, IPSET_CMD_TEST)
        ipset.parse_elem(self._session, 1, value)
        return ipset.cmd(self._session, IPSET_CMD_TEST, 0)

    def delete(self, name, value):
        ipset.parse_setname(self._session, IPSET_SETNAME, name)
        ipset.type_get(self._session, IPSET_CMD_DEL)
        ipset.parse_elem(self._session, 1, value)
        return ipset.cmd(self._session, IPSET_CMD_DEL, 0)

    def list(self, name):
        acc = ResultAccumulator()
        ipset.session_outfn(self._session, OUTFN(acc))
        ipset.parse_setname(self._session, IPSET_SETNAME, name)
        ret = ipset.cmd(self._session, IPSET_CMD_LIST, 0)
        if ret != 0:
            return []
        tree = ET.fromstring(acc.result)
        return [ e.text for e in tree.iter("elem") ]


if __name__ == "__main__":
    session = Session()
    print session

    name = "h"

    print session.list(name)
    print session.add(name, '10.0.0.1')
    print session.list(name)
    print session.test(name, '10.0.0.1')
    print session.delete(name, '10.0.0.1')
    print session.list(name)
