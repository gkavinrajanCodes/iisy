### 🗓️ **May 26 – Daily Progress Report**

**✅ Tasks Completed:**

* **Cloned and integrated** the official IIsy GitHub repository into the main project under `iisy_project/ml/`.
* Successfully **ran `main.py`** after resolving multiple dependency and versioning issues.
* Confirmed that key model artifacts (`switch_model_clf.pickle`) are generated in the `log/` directory.
* Investigated and resolved a **scikit-learn version mismatch error** during model loading by re-generating the `.pickle` file using the local environment’s version.
* Wrote and executed a script (`test.py`) to successfully **load the `switch_model_clf.pickle`** model file.
* Printed the model structure: a custom `RandomForestClassifier_Selected_Features` with `n_estimators=5`, `max_depth=8`, and `tree_features=[[0,1,2,3],...]`.

**📁 Files Verified:**

* `main.py`
* `log/switch_model_clf.pickle`
* Confirmed that the pickled model contains a simplified Random Forest classifier suitable for switch implementation.

**📌 Plan for Tomorrow (May 27):**

* Write a script (`explore_model.py`) to **extract decision rules** from each tree (features, thresholds, leaf predictions).
* Use extracted rules to **design P4 table structures** capable of mimicking these decision paths.
* Start building the `iisy.p4` program to handle classification logic.
* Begin drafting a **controller script** (`populate_tables.py`) to push model rules into BMv2 using CLI or Thrift.

**🚧 Issues Encountered:**

* Sklearn version mismatch (`1.2.2` vs `1.3.2`) when loading pickled model → resolved by retraining in the current environment.
* `main.py` required debugging but now runs correctly.

### Output for the main.py

```
features = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
fit switch model with features subset: ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
Switch confidence th=0.5: AUC 0.997737 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 0.955556 , Precision server 0.955556  , Switch Fraction 1.000000
Switch confidence th=0.52: AUC 0.997737 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 0.955556 , Precision server 0.955556  , Switch Fraction 1.000000
Switch confidence th=0.54: AUC 0.997737 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 0.955556 , Precision server 0.955556  , Switch Fraction 1.000000
Switch confidence th=0.56: AUC 0.997737 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 0.955556 , Precision server 0.955556  , Switch Fraction 1.000000
Switch confidence th=0.58: AUC 0.997737 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 0.955556 , Precision server 0.955556  , Switch Fraction 1.000000
Switch confidence th=0.6: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.62: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.64: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.66: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.68: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.7: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.72: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.74: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.76: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.78: AUC 0.996983 , Macro-F1  0.932131 , Accuracy 0.933333 , Precision 0.937951 , Recall 0.927778 , Precision switch 0.976744 , Precision server 1.000000  , Switch Fraction 0.955556
Switch confidence th=0.8: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.82: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.84: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.86: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.88: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.9: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.92: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.94: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.96: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=0.98: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
Switch confidence th=1.0: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 0.000000 , Precision server 0.000000  , Switch Fraction 0.000000
Close fig window to proceed
Switch confidence th=0.95: AUC 0.996983 , Macro-F1  0.955556 , Accuracy 0.955556 , Precision 0.955556 , Recall 0.955556 , Precision switch 1.000000 , Precision server 1.000000  , Switch Fraction 0.933333
```

### Output for the test.py to check the contents of the switch_model_clf.pickle

```
RandomForestClassifier_Selected_Features(class_weight='balanced', max_depth=8,
                                         max_features=None, n_estimators=5,
                                         n_jobs=8, random_state=42,
                                         tree_features=[[0, 1, 2, 3],
                                                        [0, 1, 2, 3],
                                                        [0, 1, 2, 3],
                                                        [0, 1, 2, 3],
                                                        [0, 1, 2, 3]])
```

### Output for the explore_model.py to find out the feature layout in the random forest

```

🌳 Tree 0
Node 0: if feature[3] <= 7.5000
Leaf Node 1: Predict class 0
Node 2: if feature[3] <= 16.5000
Node 3: if feature[2] <= 49.5000
Leaf Node 4: Predict class 1
Node 5: if feature[1] <= 24.5000
Leaf Node 6: Predict class 2
Leaf Node 7: Predict class 1
Node 8: if feature[2] <= 48.5000
Node 9: if feature[0] <= 54.0000
Leaf Node 10: Predict class 2
Leaf Node 11: Predict class 1
Leaf Node 12: Predict class 2

🌳 Tree 1
Node 0: if feature[2] <= 26.0000
Leaf Node 1: Predict class 0
Node 2: if feature[2] <= 49.5000
Node 3: if feature[3] <= 16.0000
Leaf Node 4: Predict class 1
Node 5: if feature[1] <= 31.0000
Leaf Node 6: Predict class 2
Leaf Node 7: Predict class 1
Node 8: if feature[3] <= 17.0000
Node 9: if feature[3] <= 15.5000
Leaf Node 10: Predict class 2
Leaf Node 11: Predict class 1
Node 12: if feature[0] <= 57.5000
Leaf Node 13: Predict class 2
Leaf Node 14: Predict class 2

🌳 Tree 2
Node 0: if feature[2] <= 27.0000
Leaf Node 1: Predict class 0
Node 2: if feature[3] <= 16.5000
Node 3: if feature[2] <= 49.5000
Node 4: if feature[1] <= 21.0000
Leaf Node 5: Predict class 1
Leaf Node 6: Predict class 1
Node 7: if feature[2] <= 50.5000
Leaf Node 8: Predict class 2
Leaf Node 9: Predict class 1
Node 10: if feature[0] <= 60.5000
Node 11: if feature[0] <= 58.0000
Node 12: if feature[2] <= 47.0000
Leaf Node 13: Predict class 2
Leaf Node 14: Predict class 2
Leaf Node 15: Predict class 1
Leaf Node 16: Predict class 2

🌳 Tree 3
Node 0: if feature[3] <= 7.0000
Leaf Node 1: Predict class 0
Node 2: if feature[3] <= 17.0000
Node 3: if feature[2] <= 49.5000
Node 4: if feature[3] <= 10.5000
Leaf Node 5: Predict class 1
Leaf Node 6: Predict class 1
Node 7: if feature[3] <= 15.5000
Leaf Node 8: Predict class 2
Leaf Node 9: Predict class 1
Node 10: if feature[2] <= 49.5000
Node 11: if feature[1] <= 31.0000
Leaf Node 12: Predict class 2
Leaf Node 13: Predict class 1
Leaf Node 14: Predict class 2

🌳 Tree 4
Node 0: if feature[3] <= 7.0000
Leaf Node 1: Predict class 0
Node 2: if feature[3] <= 16.5000
Node 3: if feature[2] <= 49.5000
Leaf Node 4: Predict class 1
Leaf Node 5: Predict class 2
Leaf Node 6: Predict class 2
```


Absolutely! Here's a detailed **daily prognosis** summarizing everything we’ve worked on today regarding your P4 project — including debugging, progress, and current status — suitable for adding to your daily report:

---

### **Daily Work Report — \[Date: 2025-05-27]**

**Project:** *IIsy: Hybrid In-network Classification using Programmable Switches*

#### **Objective for the Day:**

Integrate extracted classification rules from `forest_rules.json` into the BMv2 behavioral model by populating a P4 ternary match-action table using a Python-based automation script.

---

### **Tasks Completed:**

1. **BMv2 Runtime Issue Resolution**

   * Encountered and resolved a `libruntimestubs.so.0` missing shared library error when running `simple_switch`.
   * Verified the shared object path and made it accessible via `LD_LIBRARY_PATH`.

2. **P4 Program Compilation**

   * Verified that the P4 source file `classifier.p4` compiled correctly using:

     ```bash
     p4c --target bmv2 --arch v1model -o build classifier.p4
     ```

3. **Switch Execution**

   * Successfully launched `simple_switch` with the compiled JSON and appropriate interfaces.
   * Observed that the Thrift server started on port 9090, indicating readiness for runtime table programming.

4. **Populating Tables via Python Script**

   * Faced repeated errors from BMv2:

     * “**Table is ternary, but could not extract a valid priority from args**”
     * “**Table needs 4 key fields**”
   * Root cause identified: **incorrect or incomplete key formatting** and **missing priority argument** for ternary tables.

5. **Script Debugging and Enhancement**

   * Modified Python script to:

     * Ensure exactly **4 key fields** are passed per table entry.
     * Format matches in ternary form using the `value &&& mask` format.
     * Add a valid **priority value** as the final argument to each `table_add` command.

6. **Tested Updated Script**

   * New script now generates valid BMv2 runtime commands like:

     ```bash
     table_add MyIngress.classifier_table MyIngress.set_class_1 0 &&& 0 0 &&& 0 49 &&& 255 16 &&& 255 1 =>
     ```
   * Still testing individual entries due to BMv2 runtime sensitivity to malformed arguments.

---

### **Current Issues & Notes:**

* BMv2 is **strict about key ordering and formatting** for ternary tables.
* Final script compiles and prints correct commands; some entries still require testing with varied feature ranges.
* Next step: validate accuracy of match ranges and consistency of rule priority.

---

### **Next Steps:**

* Manually test generated commands via `simple_switch_CLI`.
* Validate table behavior using test packets.
* Automate packet injection and class verification to close the in-network classification loop.

---
