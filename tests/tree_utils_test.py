"""tree_utils against fake LLDB values shaped like dictionary.c's tree nodes"""

from tree_utils import DFS, print_tree, tree_size


class Null:
    """A NULL child pointer: LLDB reports its value as a zero address."""

    def GetValue(self):
        return "0x0000000000000000"


class Word:
    def __init__(self, word):
        self.word = word

    def GetSummary(self):
        return f'"{self.word}"'


class Node:
    """A tree_node {word, left, right} pointer."""

    def __init__(self, word, left=None, right=None):
        self.children = [Word(word), left or Null(), right or Null()]

    def GetValue(self):
        return hex(id(self))

    def GetChildAtIndex(self, i):
        return self.children[i]

    def GetChildMemberWithName(self, name):
        return self.children[["word", "left", "right"].index(name)]


def tree():
    #        kiwi
    #       /    \
    #   apple    pear
    #       \
    #       fig
    return Node("kiwi", Node("apple", right=Node("fig")), Node("pear"))


def test_dfs_returns_path_to_word():
    root = tree()
    assert DFS(root, "kiwi", "") == ""
    assert DFS(root, "apple", "") == "L"
    assert DFS(root, "fig", "") == "LR"
    assert DFS(root, "pear", "") == "R"


def test_dfs_strips_single_quotes():
    assert DFS(Node("'kiwi'"), "kiwi", "start") == "start"


def test_tree_size_counts_nodes():
    assert tree_size(tree()) == 4
    assert tree_size(Null()) == 0


def test_print_tree_prints_in_order(capsys):
    print_tree(tree())
    assert capsys.readouterr().out.split() == ['"apple"', '"fig"', '"kiwi"', '"pear"']
