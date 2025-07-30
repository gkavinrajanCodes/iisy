import re
from collections import defaultdict
from typing import List, Tuple

Rule = Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int], int]

def parse_rule_line(line:str)->Rule:
    parts = line.strip().split()
    idx = parts.index("set_class")
    fields = parts[idx+1:idx+9]
    class_id = int(parts[-1])
    vm_pairs = [(int(fields[i]), int(fields[i+2])) for i in range(0,8,2)]
    return (*vm_pairs, class_id)


def rule_to_str(rule: Rule) -> str:
    vals = [f"{v} &&& {m}" for (v,m) in rule[:4]]
    return f"table_add MyIngress.classifier_table set_class {' '.join(vals)} => {rule[4]}"

def merge_two_rules(rule1: Rule, rule2: Rule) -> Rule or None:
    merged = []
    for (v1, m1), (v2, m2) in zip(rule1[:4], rule2[:4]):
        if m1 != m2:
            return None
        diff = v1 ^ v2
        if diff & ~m1 != 0:
            return None
        new_mask = m1 & ~diff
        new_val = v1 & new_mask
        merged.append((new_val, new_mask))
    if rule1[4] != rule2[4]:
        return None
    return (*merged,  rule1[4])


def merge_rules_group(rules:List[Rule]) -> List[Rule]:
    changed = True
    while changed:
        changed = False
        new_rules = []
        used = [False] * len(rules)
        for i in range(len(rules)):
            if used[i]:
                continue
            for j in range(i + 1, len(rules)):
                if used[j]:
                    continue
                merged = merge_two_rules(rules[i], rules[j])
                if merged:
                    new_rules.append(merged)
                    used[i] = used[j] = True
                    changed = True
                    break
            if not used[j]:
                new_rules.append(rules[i])
                used[i] = True
        rules = new_rules
    return rules


def main():
    with open("populate_tables.txt") as f:
        lines = [line for line in f if line.strip() and "table_add" in line]

    rules = [parse_rule_line(line) for line in lines]

    groups = defaultdict(list)
    for rule in rules:
        groups[rule[4]].append(rule)
    
    merged_rules = []
    for class_id, group in groups.items():
        merged = merge_rules_group(group)
        merged_rules.extend(merged)
    
    with open("populate_tables_merged.txt", "w") as f:
        for rule in merged_rules:
            f.write(rule_to_str(rule) + "\n")
    
    print("Orignal rules = ", len(rules))
    print("Merged rules: ", len(merged_rules))

if __name__ == "main":
    main()

