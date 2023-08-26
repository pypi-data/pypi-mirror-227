import treeswift as ts
from table_fifth import TreeSet
from random import sample

treeset = TreeSet("res/avian.tre")
refs = []
with open("res/avian.tre") as f:
    for line in f:
        refs.append(ts.read_tree_newick(line))
taxa = treeset.taxa()

def naive_tally_single_quartet(trees, quartet):
    count = [0, 0, 0]
    for tree in trees:
        quartet_subtree = tree.extract_tree_with(quartet)
        for n in quartet_subtree.traverse_postorder():
            if n.is_leaf():
                n.bips = set([n.label])
            else:
                n.bips = set()
                for c in n.children:
                    n.bips.update(c.bips)
                if len(n.bips) == 2:
                    flag = False
                    if n.bips == set([quartet[0], quartet[1]]) or n.bips == set([quartet[2], quartet[3]]):
                        count[0] += 1
                    elif n.bips == set([quartet[0], quartet[2]]) or n.bips == set([quartet[1], quartet[3]]):
                        count[1] += 1
                    elif n.bips == set([quartet[0], quartet[3]]) or n.bips == set([quartet[1], quartet[2]]):
                        count[2] += 1
                    else:
                        flag = True
                    if not flag:
                        break
    return count


for r in range(10000):
    quartet_sample = sample(taxa, 4)
    distribution = treeset.tally_single_quartet(tuple(quartet_sample))
    distribution_ref = naive_tally_single_quartet(refs, tuple(quartet_sample))
    assert distribution == distribution_ref, "Error: {} != {}".format(distribution, distribution_ref)