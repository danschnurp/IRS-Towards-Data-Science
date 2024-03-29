import pandas as pd
import seaborn as sn
from matplotlib import pyplot as plt


# used edited code from https://gist.github.com/zachguo/10296432
def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth

    # Begin CHANGES
    fst_empty_cell = (columnwidth - 3) // 2 * " " + "t/p" + (columnwidth - 3) // 2 * " "

    if len(fst_empty_cell) < len(empty_cell):
        fst_empty_cell = " " * (len(empty_cell) - len(fst_empty_cell)) + fst_empty_cell
    # Print header
    print("    " + fst_empty_cell, end=" ")
    # End CHANGES

    for label in labels:
        print("%{0}s".format(columnwidth) % label, end=" ")

    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(columnwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()


def plot_cm(cm, labels):
    """
    Plot confusion matrix

    :param cm: confusion matrix
    :param labels:  labels coresponding to the confusion matrix
    """
    df_cm = pd.DataFrame(cm, labels,
                         labels)

    plt.figure(figsize=(9, 7))
    ax = plt.subplot()
    g = sn.heatmap(df_cm, square=True, cmap="Blues", annot=True, fmt='g', ax=ax)
    g.set_yticklabels(rotation=30, labels=labels)
    ax.set_xlabel('Predicted labels', fontweight='demi')
    ax.set_ylabel('True labels', fontweight='demi')
    ax.set_title('Language detection Confusion Matrix')
    plt.tight_layout()
    plt.show()
