#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<8> PROTO_TCP = 6;

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


struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    tcp_t tcp;
}



struct metadata {
    bit<8> classification;
}


parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata)
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
                        transition select(hdr.ipv4.protocol){
                            PROTO_TCP: parse_tcp;
                            default: accept;
                        }
                    }
                    state parse_tcp {
                        packet.extract(hdr.tcp);
                        transition accept;
                    }
                }


control MyVerifyCheckSum(inout headers hdr, inout metadata meta)
{
	apply { }
}


control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata)
                  {
                    action set_class_0() {
                        meta.classification = 0;
                    }
                    action set_class_1() {
                        meta.classification = 1;
                    }
                    action _nop() {
                        // no-op 
                    }
                    table classifier_table {
                        key = {
                            hdr.tcp.dstPort: ternary;
                        }
                        actions = {
                            set_class_0;
                            set_class_1;
                            _nop;
                        }
                        size = 4;
                        default_action = _nop();
                    }
                    apply {
                        classifier_table.apply();
                        standard_metadata.egress_spec = 1;
                    }
                  }

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata)
                 {
                    apply { }
                 }

control MyComputeChecksum(inout headers hdr,
                          inout metadata meta)
                          {
                            apply { }
                          }

control MyDeparser(packet_out packet,
                   in headers hdr)
                   {
                    apply {
                        packet.emit(hdr.ethernet);
                        packet.emit(hdr.ipv4);
                        packet.emit(hdr.tcp);
                    }
                   }

V1Switch(MyParser(), MyVerifyCheckSum(), MyIngress(), MyEgress(), MyComputeChecksum(), MyDeparser()) main;