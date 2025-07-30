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

struct metadata_t {
    bit<3> feature_0;
    bit<3> feature_1;
    bit<1> feature_2;
    bit<1> feature_3;
    bit<2> predicted_class;
}

struct headers_t {
    ethernet_t ethernet;
    ipv4_t ipv4;

}

parser MyParser(packet_in packet,
                out headers_t hdr,
                inout metadata_t meta,
                inout standard_metadata_t stdmeta)
                {
                    state start {
                        packet.extract(hdr.ethernet);
                        transition select(hdr.ethernet.etherType)
                        {
                            TYPE_IPV4: parse_ipv4;
                            default: accept;
                        }
                    }
                    state parse_ipv4 {
                        packet.extract(hdr.ipv4);
                        meta.feature_0 = hdr.ipv4.diffserv[7:5];
                        meta.feature_1 = hdr.ipv4.diffserv[4:2];
                        meta.feature_2 = hdr.ipv4.diffserv[1:1];
                        meta.feature_3 = hdr.ipv4.diffserv[0:0];
                        
                        transition accept;
                    }
                }

control MyVerifyCheckSum(inout headers_t hdr, inout metadata_t meta) {
    apply { }
}

control MyComputeChecksum(inout headers_t hdr, inout metadata_t meta) {
    apply { }
}


control MyIngress(inout headers_t hdr,
                  inout metadata_t meta, 
                  inout standard_metadata_t stdmeta)
                  {
                    action set_class(bit<2> class_id)
                    {
                        meta.predicted_class = class_id;
                    }
                    action _nop() {
                        //no action
                    }
                    table classifier_table {
                        key = {
                            meta.feature_0: ternary;
                            meta.feature_1: ternary;
                            meta.feature_2: ternary;
                            meta.feature_3: ternary;
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

control MyEgress(inout headers_t hdr,
                 inout metadata_t meta,
                 inout standard_metadata_t stdmeta)
                 {
                    apply {

                    }
                 }

control MyDeparser(packet_out packet,
                   in headers_t hdr)
                   {
                    apply {
                        packet.emit(hdr.ethernet);
                        packet.emit(hdr.ipv4);
                    }
                   }

V1Switch(MyParser(), MyVerifyCheckSum(), MyIngress(), MyEgress(), MyComputeChecksum(), MyDeparser()) main;






