# -*- coding: utf-8 -*-
"""C4_5_Algorithm_code DT & PR.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Tf3rOXcmVs5oSNaCwS08BBna6PKvVBew
"""

from graphviz import Digraph
import matplotlib.pyplot as plt
import math
import pandas as pd
from math import log2
import numpy as np
import copy

class TreeNode:
    def __init__(self, label=None, attribute=None, branches=None):
        self.label = label
        self.attribute = attribute
        self.branches = branches or {}

    def get_label(self):
        if self.label is not None:
            return str(self.label)
        elif self.attribute is not None:
            return str(self.attribute)
        else:
            return ""

    def is_leaf(self):
        return not bool(self.branches)

    def add_to_dot(self, dot):
        node_id = str(id(self))
        label = str(self.get_label())  # Ensure label is a string

        if self.is_leaf():
            # Set shape to rectangle for leaf nodes
            dot.node(node_id, label=label, shape='rectangle')
        else:
            dot.node(node_id, label=label)

        for branch_label, branch in self.branches.items():
            branch.add_to_dot(dot)
            dot.edge(node_id, str(id(branch)), label=str(branch_label))  # Ensure branch label is a string

    def add_to_flow(self, flow):
        if self.is_leaf():
            flow.text(self.get_label())
        else:
            for branch_label, branch in self.branches.items():
                with flow.expander(str(branch_label)):
                    branch.add_to_flow(flow)

def c45(examples, target_attribute, attributes, validation_data=None, root=None):
    print(attributes_dict)
    root = TreeNode()

    # If all examples are positive, return a single-node tree with label = 'Play'
    if all(example[target_attribute] == 'Pass' for example in examples if example['weight'] == 1 or example['weight'] == 0):
        weight_sum = sum(example['weight'] for example in examples)
        error_sum = sum(example['weight'] for example in examples if not (example[target_attribute] == 'Pass'))
        root.label = f'Pass ({weight_sum:.1f}/{error_sum:.1f})'

    # If all examples are negative, return a single-node tree with label = "Don't Play"
    elif all(example[target_attribute] == 'Fail' for example in examples if example['weight'] == 1 or example['weight'] == 0):
        weight_sum = sum(example['weight'] for example in examples)
        error_sum = sum(example['weight'] for example in examples if not (example[target_attribute] == 'Fail'))
        root.label = f'Fail ({weight_sum:.1f}/{error_sum:.1f})'

    # If attributes is empty, return a single-node tree with label = most common value of Targetattribute
    elif not attributes:
        root.label = most_common_value(examples, target_attribute)

    else:
        # Choose the best attribute to split on
        best_attribute, threshold = choose_best_attribute(examples, target_attribute, attributes)

        examples_with_nan = [example for example in examples if pd.isna(example.get(best_attribute))]
        examples_not_nan = [example for example in examples if not pd.isna(example.get(best_attribute))]
        len_of_not_null = len(examples_not_nan)

        for example in examples_not_nan:
            if example['weight'] == 0:
                example['weight'] = 1
            else:
                example['weight'] *= 1

        # Split the examples based on the chosen attribute
        subsets = {}
        if attribute_type_mapping[best_attribute] == 0:
            root.attribute = best_attribute
            attribute_values = attributes_dict[best_attribute]
            for value in attribute_values:
                subsets[value] = [example for example in examples_not_nan if example[best_attribute] == value]
                len_of_attr_val = sum(1 for example in examples_not_nan if example[best_attribute] == value)
                if len_of_not_null != 0:
                    w = len_of_attr_val/len_of_not_null
                    ex_copy = copy.deepcopy(examples_with_nan)
                    for example in ex_copy:
                        example['weight'] = w

                    subsets[value].extend(ex_copy)
                else:
                    subsets[value] = [example for example in examples_with_nan if example[best_attribute] == value]
        else:
            subsets['yes'] = [example for example in examples if float(example[best_attribute]) <= threshold]
            subsets['no'] = [example for example in examples if float(example[best_attribute]) > threshold]
            best_attribute = f"{best_attribute} <= {threshold}"
            root.attribute = best_attribute
            attributes_dict[best_attribute] = ['yes', 'no']

        for value in subsets:
            if not subsets[value]:
                # If subset is empty, add a leaf node with label = most common value of Targetattribute
                leaf = TreeNode(label=most_common_value(examples, target_attribute))
                root.branches[value] = leaf
            else:
                # Recursively add subtree
                subtree = c45(subsets[value], target_attribute, [attr for attr in attributes if attr != best_attribute])
                root.branches[value] = subtree

    return root

def most_common_value(examples, target_attribute):
    # Return the most common value of the target attribute in the given examples
    positive_count = sum(1 for example in examples if example[target_attribute] == 'Pass')
    negative_count = sum(1 for example in examples if example[target_attribute] == "Fail")
    return 'Pass' if positive_count >= negative_count else "Fail"

# Function to compute entropy of a set
def compute_entropy(labels):
    unique_labels = labels.unique()
    entropy = 0.0

    for label in unique_labels:
        prob = (labels == label).sum() / len(labels)
        if prob != 0:
            entropy -= prob * log2(prob)

    return entropy

# Function to compute entropy of a split
def compute_split_entropy(left_labels, right_labels, target_column):
    total_length = len(left_labels) + len(right_labels)
    left_weight = len(left_labels) / total_length
    right_weight = len(right_labels) / total_length

    left_entropy = compute_entropy(left_labels[target_column])
    right_entropy = compute_entropy(right_labels[target_column])

    split_entropy = left_weight * left_entropy + right_weight * right_entropy
    return split_entropy

# Function to compute split information for gain ratio
def compute_split_info(left_subset, right_subset, continuous_attribute):
    total_length = len(left_subset) + len(right_subset)
    left_weight = len(left_subset) / total_length
    right_weight = len(right_subset) / total_length

    left_values = left_subset[continuous_attribute].unique()
    right_values = right_subset[continuous_attribute].unique()

    left_info = -sum((len(left_subset[left_subset[continuous_attribute] == value]) / len(left_subset)) * log2(len(left_subset[left_subset[continuous_attribute] == value]) / len(left_subset)) for value in left_values if len(left_subset[left_subset[continuous_attribute] == value]) > 0)

    right_info = -sum((len(right_subset[right_subset[continuous_attribute] == value]) / len(right_subset)) * log2(len(right_subset[right_subset[continuous_attribute] == value]) / len(right_subset)) for value in right_values if len(right_subset[right_subset[continuous_attribute] == value]) > 0)

    split_info = left_weight * left_info + right_weight * right_info
    return split_info

def compute_categorical_gain_ratio(subset, target_column, attribute):
    subset = pd.DataFrame(subset)
    initial_entropy = compute_entropy(subset[target_column])

    # Extract unique values of the 'attribute' from a subset, remove occurrences of 'nan', and calculates the fraction (F) of non-'nan' values
    attribute_values = subset[attribute].unique()
    attribute_values_without_nan = attribute_values[pd.notna(attribute_values)]
    F = len(attribute_values_without_nan)/len(attribute_values)

    weighted_entropy = 0.0
    split_info = 0.0
    gives_a_pure_node = False

    for value in attribute_values_without_nan:
        if pd.isna(value):
            value_subset = subset[pd.isna(subset[attribute])]
        else:
            value_subset = subset[subset[attribute] == value]
        value_weight = len(value_subset) / len(subset)

        value_entropy = compute_entropy(value_subset[target_column])
        weighted_entropy += value_weight * value_entropy
        # To find whether there is pure split in atleast one node
        if value_entropy == 0:
            gives_a_pure_node = True

        split_info -= value_weight * log2(value_weight)

    gain = F*(initial_entropy - weighted_entropy)
    # print("Gain ====",attribute, " : ", gain)
    gain_ratio = gain / split_info if split_info != 0 else 0.0

    return gain_ratio, gives_a_pure_node, gain


def calculate_continuous_gain_ratio(examples, target_attribute, attribute):

    # Specify the continuous attribute and the target column
    continuous_attribute = attribute
    target_column = target_attribute

    df = pd.DataFrame(examples)

    # Sort the DataFrame based on the continuous attribute
    df_sorted = df.sort_values(by=continuous_attribute)

    # Compute initial entropy before the split
    initial_entropy = compute_entropy(df_sorted[target_column])

    # Initialize variables to keep track of best split
    best_gain_ratio = 0.0
    best_threshold = None

    # Iterate through possible split points
    for i in range(1, len(df_sorted)):
        #if df_sorted.iloc[i - 1][continuous_attribute] == df_sorted.iloc[i][continuous_attribute]:
        #    continue
        threshold = (float(df_sorted.iloc[i - 1][continuous_attribute]) + float(df_sorted.iloc[i][continuous_attribute])) / 2.0

        # Split the data into two subsets based on the threshold
        left_subset = df_sorted[df_sorted[continuous_attribute] <= threshold]
        right_subset = df_sorted[df_sorted[continuous_attribute] > threshold]

        # Calculate gain and split information for the current split
        gain = initial_entropy - compute_split_entropy(left_subset, right_subset, target_column)
        split_info = compute_split_info(left_subset, right_subset, continuous_attribute)

        # Calculate gain ratio
        gain_ratio = gain / split_info if split_info != 0 else 0.0

        # Update best split if gain ratio is higher
        if gain_ratio > best_gain_ratio:
            best_gain_ratio = gain_ratio
            best_threshold = threshold

    # Return the maximum gain ratio
    return best_gain_ratio, best_threshold

def choose_best_attribute(examples, target_attribute, attributes):
    best_attribute = None
    best_gain_ratio = -1
    threshold = -1
    gain_threshold_list = {}
    gives_a_pure_node = False
    attr_gain = {}
    attr_gain_ratio = {}

    for attribute in attributes:
        # Check if the attribute is continuous
        if attribute_type_mapping[attribute] == 1:
            gain_ratio, threshold = calculate_continuous_gain_ratio(examples, target_attribute, attribute)
            gain_threshold_list[gain_ratio] = threshold

        else:
            gain_ratio, gives_a_pure_node, gain = compute_categorical_gain_ratio(examples, target_attribute, attribute)
            gain_threshold_list[gain_ratio] = threshold

        attr_gain[attribute] = gain
        attr_gain_ratio[attribute] = gain_ratio

        if (threshold != -1 or True) and gain_ratio > best_gain_ratio:
            best_gain_ratio = gain_ratio
            best_attribute = attribute
    # if best_attribute == "|Portfolio Return| > 8":
    #    best_attribute = "|Portfolio Return| > 5"
    print("\nBest attribute: ", best_attribute, " : ", best_gain_ratio)

    sorted_attr_gain = sorted(attr_gain.items(), key=lambda item: item[1], reverse=True)
    for key, value in sorted_attr_gain[:3]:
        print(f"Gain: {key} {value}")
    sorted_attr_gain_ratio = sorted(attr_gain_ratio.items(), key=lambda item: item[1], reverse=True)
    for key, value in sorted_attr_gain_ratio[:3]:
        print(f"Gain Ratios: {key} {value}")

    # sort the attr_gain by values and print top 3


    return best_attribute, gain_threshold_list[best_gain_ratio]

def print_leaf(node):
    leaves = []  # Use a Python list, not a NumPy array

    if node.label is not None:
        return [node.label]  # Return a list with the label

    for value, subtree in node.branches.items():
        leaves.extend(print_leaf(subtree))  # Use extend instead of append

    return leaves

def tree_to_rules(node, indent=0, rule_list=None, current_rule=None):
    if rule_list is None:
        rule_list = []

    if current_rule is None:
        current_rule = ""

    if node.label is not None:
        rule_list.append(current_rule + node.label)
    else:
        for value, subtree in node.branches.items():
            new_rule = current_rule + f"If {node.attribute} is {str(value).upper()} then "
            tree_to_rules(subtree, indent + 1, rule_list, new_rule)

    return rule_list


# Initialize the attribute type mapping dictionary
attribute_type_mapping = {}
attributes_dict = {}
def build_tree(df):
    global attributes_dict
    
    # Remove the columns that does not participate in classification
    df = df.drop(['Portfolio Type'], axis = 1)

    # Example attributes and target_attribute
    attributes = df.columns[:-1].tolist()
    target_attribute = df.columns[-1]

    # Adding a column named "weight" with default values of 0
    df['weight'] = 0

    # Create a dictionary with unique attribute values
    attrs_dict = {col: df[col].dropna().unique().tolist() for col in df.columns}
    attributes_dict = attrs_dict

    # Iterate over columns and classify attributes
    for attribute in df.columns:
        # Check if an attribute is categorical or continuous
        is_float = pd.to_numeric(df[attribute], errors='coerce').notnull().all()
        num_unique_values = df[attribute].nunique()

        if is_float and num_unique_values > 2:
            attribute_type_mapping[attribute] = 1  # Continuous
        else:
            attribute_type_mapping[attribute] = 0  # Categorical

    # Example usage
    tree = c45(df.to_dict(orient='records'), target_attribute, attributes)

    return tree
