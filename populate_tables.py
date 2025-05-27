import json
import subprocess

CLI_PATH = "/usr/local/bin/simple_switch_CLI"
P4_TABLE = "MyIngress.classifier_table"
P4_ACTIONS = [
    "MyIngress.set_class_0",
    "MyIngress.set_class_1",
    "MyIngress.set_class_2"
]

def ternary_match(low, high):
    # Return (value, mask) for ternary match
    if low == 0 and high == 255:
        return "0", "0"  # wildcard
    if low == high:
        return str(low), "255"  # exact match
    # TODO: Better range matching (for now, fallback to exact low)
    return str(low), "255"

def build_command(rule, priority):
    lows = [0] * 4
    highs = [255] * 4

    for (index, op, value) in rule['conditions']:
        try:
            v = int(round(float(value)))  # safely handle float
        except ValueError:
            raise Exception(f"Invalid value in rule: {value}")
        
        if op == "<=":
            highs[index] = min(highs[index], v)
        elif op == ">":
            lows[index] = max(lows[index], v + 1)

    # Convert to (value, mask) ternary strings
    matches = [ternary_match(lows[i], highs[i]) for i in range(4)]

    # Create key string with separate value and mask for each field
    keys = []
    for val, mask in matches:
        keys.append(val)
        keys.append(mask)

    action = P4_ACTIONS[rule['class']]
    key_str = " ".join(keys)

    return f"table_add {P4_TABLE} {action} {key_str} {priority}"

def main():
    try:
        with open("log/forest_rules.json") as f:
            forest = json.load(f)
    except Exception as e:
        print(f"Error loading forest_rules.json: {e}")
        return

    priority = 1
    for tree_id, rules in enumerate(forest):
        for rule_id, rule in enumerate(rules):
            try:
                cmd = build_command(rule, priority)
                print(f"Executing: {cmd}")
                process = subprocess.Popen([CLI_PATH],
                                           stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           text=True)
                out, err = process.communicate(input=cmd + "\n")
                if out.strip():
                    print(out)
                if err.strip():
                    print("Error:", err)
                if process.returncode != 0:
                    print(f"Command failed (priority {priority})")
                priority += 1
            except Exception as e:
                print(f"Error processing rule {rule_id} in tree {tree_id}: {e}")

if __name__ == "__main__":
    main()
