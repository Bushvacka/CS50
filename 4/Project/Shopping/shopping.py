import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - (0)Administrative, an integer
        - (1)Administrative_Duration, a floating point number
        - (2)Informational, an integer
        - (3)Informational_Duration, a floating point number
        - (4)ProductRelated, an integer
        - (5)ProductRelated_Duration, a floating point number
        - (6)BounceRates, a floating point number
        - (7)ExitRates, a floating point number
        - (8)PageValues, a floating point number
        - (9)SpecialDay, a floating point number
        - (10)Month, an index from 0 (January) to 11 (December)
        - (11)OperatingSystems, an integer
        - (12)Browser, an integer
        - (13)Region, an integer
        - (14)TrafficType, an integer
        - (15)VisitorType, an integer 0 (not returning) or 1 (returning)
        - (16)Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
        for line in reader:
            user = []
            for i in range(17):
                #Why does python not have a switch statement?? Am I missing something?
                if i in [0, 2, 4, 11, 12, 13, 14]:
                    user.append(int(line[i]))
                elif i in [1, 3, 5, 6, 7, 8, 9]:
                    user.append(float(line[i]))
                elif i == 10:
                    user.append(MONTHS.index(line[i]))
                elif i == 15:
                    user.append(1 if line[i] == "Returning_Visitor" else 0)
                else:
                    user.append(1 if line[i] == "TRUE" else 0)
            evidence.append(user)
            labels.append(1 if line[17] == "TRUE" else 0)
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    pos_total = 0
    pos_right = 0
    neg_total = 0
    neg_right = 0
    for label, prediction in zip(labels, predictions):
        if prediction == 1:
            pos_total +=1
            if label == 1:
                pos_right += 1
        else:
            neg_total += 1
            if label == 0:
                neg_right += 1
    return (pos_right/pos_total, neg_right/neg_total)


if __name__ == "__main__":
    main()
