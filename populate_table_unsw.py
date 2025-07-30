import json

with open("forest_rules_unsw.json") as f:
    forest = json.load(f)

commands = []

def encode_value(value, bits = 8):
    scaled = int(round(value*10))
    return min(scaled, (1<<bits)-1)

for tree in forest:
    for rule in tree['rules']:
        key_parts = []
        mask_parts = []

        for cond in rule['conditions']:
            feature, op, threshold = cond
            fid = int(feature.split("_")[1])
            encoded = encode_value(threshold)
            if op == "<=":
                key = 0
                mask = 0
            else:
                key = encoded
                mask = 255
            key_parts.append(f"{key}")
            mask_parts.append(f"{mask}")



        while len(key_parts) < 4:
            key_parts.append("0")
            mask_parts.append("0")

        class_id = rule["class"]
        cmd = f"table_add MyIngress.classifier_table set_class {' '.join([f'{k} &&& {m}' for k, m in zip(key_parts, mask_parts)])} => {class_id}"
        commands.append(cmd)

with open("commands_unsw.txt", "w") as f:
    for cmd in commands:
        f.write(cmd + '\n')

print("Saved commands in commands_unsw.txt")

