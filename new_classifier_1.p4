#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4> version;
    bit<4> ihl;
    bit<8> diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3> flags;
    bit<13> fragOffset;
    bit<8> ttl;
    bit<8> protocol;
    bit<16> hdrChecksum;
    bit<32> srcAddr;
    bit<32> dstAddr;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4> dataOffset;
    bit<4> res;
    bit<8> flags;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}

struct metadata_t {
    bit<8> class_result;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    tcp_t tcp;
}


parser MyParser(
    packet_in packet,
    out headers hdr,
    inout metadata_t meta,
    inout standard_metadata_t standard_metadata
)
{
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            6: parse_tcp;
            default: accept;
        }
    }
    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }
}


control MyVerifyCheckSum(inout headers hdr, inout metadata_t meta) {
    apply { }
}

control MyComputeChecksum(inout headers hdr, inout metadata_t meta) {
    apply { }
}

control MyIngress(
    inout headers hdr,
    inout metadata_t meta,
    inout standard_metadata_t standard_metadata
)
{
    action set_class(bit<8> class_value) {
        meta.class_result = class_value;
    }
    action _nop() {
        // no-op 
    }
    table classifier_table {
        key = {
            hdr.tcp.srcPort: ternary;
            hdr.tcp.dstPort: ternary;
        }
        actions = {
            set_class;
            _nop;
        }
        size = 1024;
        default_action = _nop();
    }
    apply {
        classifier_table.apply();
    }
}


control MyEgress(inout headers hdr,
                 inout metadata_t meta,
                 inout standard_metadata_t standard_metadata)
                 {
                    apply { 
/*                      if (hdr.ethernet.etherType == UNDEFINED) // one extra ethernet type condition after the packet has been parsed, similar to the tcp urgent pointer -> need to keep track of the false bits and remove those packets 
                        {
                            transition select(hdr.ethernet.etherType = STANDARD) {
                                TYPE_IPV4: parse_ipv4;
                                default: accept;
                            }
*/                      }
                    }
                 }

control MyDeparser(
    packet_out packet, 
    in headers hdr
)
{
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
    }
}

V1Switch(MyParser(), MyVerifyCheckSum(), MyIngress(), MyEgress(), MyComputeChecksum(), MyDeparser()) main;








