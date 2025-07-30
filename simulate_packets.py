import json

with open("log/forest_rules.json") as f:
    forest = json.load(f)

def match_rule(packet, rule):
    for (index, op, value) in rule['conditions']:
        val = float(value)
        if op == "<=":
            if not packet[index] <= val:
                return False
        elif op == ">":
            if not packet[index] > val:
                return False
    return True

def simulate(packet, forest):
    for rules in forest:
        for rule in rules:
            if match_rule(packet, rule):
                return rule['class']
    return 0

def main():
    test_packets = [
        [50,20,10,5],
        [200,200,100,5],
        [0,0,0,0],
        [255,255,255,255],
        [30,10,5,1],
    ]


    print("\n----Print simulation----")
    for i, pkt in enumerate(test_packets):
        predicted_class = simulate(pkt, forest)
        print(f"[Packet{i+1}] features = {pkt} -> predicted_class = {predicted_class}")
    print("\n-----End simulation-----")

if __name__ == "__main__":
    main()
    