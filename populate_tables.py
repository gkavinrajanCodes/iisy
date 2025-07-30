import json

def float_to_byte(val, scale = 100):
    return int(val * scale) & 0xFF

def build_match_keys(rule):
    keys = []
    all_features = {"feature_0":None, "feature_1":None, "feature_2":None, "feature_3":None}

    for feature,op,threshold in rule["conditions"]:
        all_features[feature] = (op, threshold)

    for fname in sorted(all_features.keys()):
        if all_features[fname] is None:
            keys.append(("0x00", "0x00"))
        else:
            op, threshold = all_features[fname]
            val = float_to_byte(threshold)
            if op == "<=":
                keys.append((f"0x{val:02x}", "0xFF"))
            elif op == ">":
                keys.append((f"0x{val+1:02x}", "0xFF"))
    return keys

with open("forest_rules_iris.json") as f:
    forest= json.load(f)

with open("populate_tables.txt", "w") as out:
    for tree in forest:
        for rule in tree["rules"]:
            keys = build_match_keys(rule)
            class_id = rule["class"]
            key_str= " ".join(f"{k} &&& {m}" for k,m in keys)
            out.write(f"table_add MyIngress.classifier_table set_class {key_str} => {class_id}\n")
