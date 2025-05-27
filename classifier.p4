// classifier.p4
#include <v1model.p4>

const bit<8> CLASS_0 = 0;
const bit<8> CLASS_1 = 1;
const bit<8> CLASS_2 = 2;

header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<32> srcAddr;
    bit<32> dstAddr;
    bit<8>  protocol;
    bit<8>  ttl;
}

struct metadata_t {
    bit<8> feature_0;
    bit<8> feature_1;
    bit<8> feature_2;
    bit<8> feature_3;
    bit<8> predicted_class;
}

struct headers {
    ethernet_t ethernet;
    ipv4_t     ipv4;
}

parser MyParser(packet_in packet, out headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x0800: parse_ipv4;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }
}

control MyIngress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {

    action set_class_0() {
        meta.predicted_class = CLASS_0;
    }

    action set_class_1() {
        meta.predicted_class = CLASS_1;
    }

    action set_class_2() {
        meta.predicted_class = CLASS_2;
    }

    table classifier_table {
        key = {
            meta.feature_0: ternary;
            meta.feature_1: ternary;
            meta.feature_2: ternary;
            meta.feature_3: ternary;
        }
        actions = {
            set_class_0;
            set_class_1;
            set_class_2;
        }
        size = 1024;
        default_action = set_class_0();
    }

    apply {
        classifier_table.apply();
    }
}

control MyEgress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    apply { }
}

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
    }
}

control NoOpVerifyChecksum(inout headers hdr, inout metadata_t meta) {
    apply { }
}

control NoOpComputeChecksum(inout headers hdr, inout metadata_t meta) {
    apply { }
}

V1Switch(MyParser(), NoOpVerifyChecksum(), MyIngress(), MyEgress(), NoOpComputeChecksum(), MyDeparser()) main;
