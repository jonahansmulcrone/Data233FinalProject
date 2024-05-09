# name 1: Jonah Mulcrone
# name 2: Emmanuel Obikwelu
# name 3: Brian Sung


from typing import List, NamedTuple, Union, Any
from typing import Dict, TypeVar
from collections import Counter, defaultdict
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import math

# Define a class for the iris dataset
class IrisSample(NamedTuple):
    sepal_width: float
    petal_length: float
    petal_width: float
    star: int

# Load the iris dataset
def load_iris_data() -> List[IrisSample]:
    iris = datasets.load_iris()
    x= iris['data']
    y= iris['target']
    target_names = iris['target_names']

    iris_samples = []
    for i in range(len(x)):
        sepal_length, sepal_width, petal_length, petal_width = x[i]
        species = target_names[y[i]]
        iris_samples.append(IrisSample(sepal_length, sepal_width, petal_length, petal_width, species))

    return iris_samples

# nctions for entropy calculations
def entropy(class_probabilities: List[float]) -> float:
    return sum(-p * math.log(p, 2) for p in class_probabilities if p > 0)

def class_probabilities(labels: List[Any]) -> List[float]:
    total_count = len(labels)
    return [count / total_count for count in Counter(labels).values()]

def data_entropy(labels: List[Any]) -> float:
    return entropy(class_probabilities(labels))

def partition_entropy(subsets: List[List[Any]]) -> float:
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) * len(subset) / total_count for subset in subsets)


def partition_by(inputs: List[IrisSample], attribute: str) -> Dict[Any, List[IrisSample]]:
    partitions = defaultdict(list)
    for input in inputs:
        key = getattr(input, attribute)
        partitions[key].append(input)
    return partitions

def partition_entropy_by(inputs: List[IrisSample], attribute: str, label_attribute: str) -> float:
    partitions = partition_by(inputs, attribute)
    labels = [[getattr(input, label_attribute) for input in partition] for partition in partitions.values()]
    return partition_entropy(labels)


class Leaf(NamedTuple):
    value: Any

class Split(NamedTuple):
    attribute: str
    subtrees: dict
    default_value: Any = None

DecisionTree = Union[Leaf, Split]

def classify(tree: DecisionTree, input: IrisSample) -> Any:
    if isinstance(tree, Leaf):
        return tree.value
    subtree_key = getattr(input, tree.attribute)
    if subtree_key not in tree.subtrees:
        return tree.default_value
    subtree = tree.subtrees[subtree_key]
    return classify(subtree, input)

def build_tree_id3(inputs: List[IrisSample], split_attributes: List[str], target_attribute: str) -> DecisionTree:
    label_counts = Counter(getattr(input, target_attribute) for input in inputs)
    most_common_label = label_counts.most_common(1)[0][0]

    if len(label_counts) == 1:
        return Leaf(most_common_label)

    if not split_attributes:
        return Leaf(most_common_label)

    def split_entropy(attribute: str) -> float:
        return partition_entropy_by(inputs, attribute, target_attribute)

    best_attribute = min(split_attributes, key=split_entropy)

    partitions = partition_by(inputs, best_attribute)
    new_attributes = [a for a in split_attributes if a != best_attribute]

    subtrees = {attribute_value: build_tree_id3(subset, new_attributes, target_attribute)
                for attribute_value, subset in partitions.items()}

    return Split(best_attribute, subtrees, default_value=most_common_label)

# load iris dataset
iris_data = load_iris_data()

# Define attributes and target attribute
split_attributes = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
target_attribute = 'species'

# Build decision tree
iris_tree = build_tree_id3(iris_data, split_attributes, target_attribute)

# Make predictions for the given data points
data_points = [
    IrisSample(6.0, 3.0, 5.0, 0.6, ''),  # Add empty string as a placeholder for species
    IrisSample(6.0, 3.0, 5.0, 1.6, ''),
    IrisSample(6.0, 3.0, 5.0, 2.6, ''),
    IrisSample(5.1, 3.5, 1.4, 0.2, ''),
    IrisSample(4.9, 3.0, 1.4, 0.2, '')
]

predictions = [classify(iris_tree, data_point) for data_point in data_points]

print("Predictions:", predictions)

# Load iris dataset
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Train decision tree classifier
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Make predictions
new_samples = [
    [6.0, 3.0, 5.0, 0.6],
    [6.0, 3.0, 5.0, 1.6],
    [6.0, 3.0, 5.0, 2.6],
    [5.1, 3.5, 1.4, 0.2],
    [4.9, 3.0, 1.4, 0.2]
]
predictions = clf.predict(new_samples)
taget = iris.target_names[predictions]
print("Predictions2:", taget)
