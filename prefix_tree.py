"""CSC148 Assignment 2: Autocompleter classes

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains the design of a public interface (Autocompleter) and two
implementation of this interface, SimplePrefixTree and CompressedPrefixTree.
You'll complete both of these subclasses over the course of this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
from typing import Any, List, Optional, Tuple


################################################################################
# The Autocompleter ADT
################################################################################
class Autocompleter:
    """An abstract class representing the Autocompleter Abstract Data Type.
    """
    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """
        raise NotImplementedError

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# SimplePrefixTree (Tasks 1-3)
################################################################################
class SimplePrefixTree(Autocompleter):
    """A simple prefix tree.

    This class follows the implementation described on the assignment handout.
    Note that we've made the attributes public because we will be accessing them
    directly for testing purposes.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.
    weight_type:
        a string that is either sum or average and this determines how to add
        the weights

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - ("prefixes grow by 1")
      If len(self.subtrees) > 0, and subtree in self.subtrees, and subtree
      is non-empty and not a leaf, then

          subtree.value == self.value + [x], for some element x

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Any
    weight: float
    subtrees: List[SimplePrefixTree]
    weight_type: str

    def __init__(self, weight_type: str) -> None:
        """Initialize an empty simple prefix tree.

        Precondition: weight_type == 'sum' or weight_type == 'average'.

        The given <weight_type> value specifies how the aggregate weight
        of non-leaf trees should be calculated (see the assignment handout
        for details).
        """
        self.weight_type = weight_type
        self.weight = 0.0
        self.subtrees = []
        self.value = []

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        return self.weight == 0.0

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        return self.weight > 0 and self.subtrees == []

    def __str__(self) -> str:
        """Return a string representation of this tree.

        You may find this method helpful for debugging.
        """

        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.value} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        if self.weight == 0:
            return 0
        elif self.subtrees == [] and self.weight > 0:
            return 1
        else:
            length = 0
            for subtree in self.subtrees:
                length += subtree.__len__()
            return length

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """
        if self.weight == 0:
            if len(prefix) == 0:
                new = SimplePrefixTree(self.weight_type)
                new.value = value
                new.weight = weight
                self.weight = weight
                self.subtrees.append(new)
            else:
                new = SimplePrefixTree(self.weight_type)
                for item in self.value:
                    new.value.append(item)
                new.value.append(prefix[0])
                self.subtrees.append(new)
                new.insert(value, weight, prefix[1:])
                self.weight = weight

        else:
            check = False
            for subtree in self.subtrees:
                if prefix[:len(subtree.value)] == subtree.value:
                    check = True
                    break

            # if the prefix is not in there
            if check is False:
                self._simple_insert_help(value, weight, prefix)

            # if it  is in there
            else:
                for subtree in self.subtrees:
                    if subtree.value == prefix[:len(subtree.value)]:
                        subtree.insert(value, weight, prefix)

            # updates weights
            if self.weight_type == 'sum':
                sum_weight = 0
                for subtree in self.subtrees:
                    sum_weight += subtree.weight
                self.weight = sum_weight
            else:
                acc = 0
                for tree in self.subtrees:
                    acc += tree.weight * tree.__len__()
                self.weight = acc / self.__len__()

    def _simple_insert_help(self, value: Any, weight: float, prefix: List) -> \
            None:
        """
        if tree is Non empty and the prefix is not in subtrees
        """
        new = SimplePrefixTree(self.weight_type)
        if len(self.value) + 1 > len(prefix):
            check_value = False
            for subtree in self.subtrees:
                if subtree.value == value:
                    check_value = True
            if check_value is False:
                new.value = value
                new.weight = weight
                self.subtrees.append(new)
                self.subtrees.sort(key=lambda x: x.weight, reverse=True)
            else:
                for subtree in self.subtrees:
                    if subtree.value == value:
                        subtree.weight += weight
        else:
            new.value = self.value + [prefix[len(self.value)]]
            self.subtrees.append(new)
            new.insert(value, weight, prefix[len(new.value):])
            self.subtrees.sort(key=lambda x: x.weight, reverse=True)

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """
        new = []
        if self.weight == 0:
            return []
        else:
            for subtree in self.subtrees:
                if len(new) == limit:
                    break
                elif subtree.is_leaf() and self.value[:len(prefix)] == prefix:
                    new.append((subtree.value, subtree.weight,))
                elif subtree.value == prefix[:len(subtree.value)]:
                    if limit is not None:
                        new.extend(
                            subtree.autocomplete(prefix, limit - len(new)))
                    else:
                        new.extend(
                            subtree.autocomplete(prefix, limit))
                elif len(prefix) < len(subtree.value):
                    if subtree.value[:len(prefix)] == prefix:
                        self._simple_auto_help(new, prefix, subtree, limit)

        new.sort(key=lambda x: x[1], reverse=True)
        return new

    @staticmethod
    def _simple_auto_help(new: List, prefix: List, subtree: SimplePrefixTree,
                          limit: Optional[int] = None)-> None:
        """
        update weights when inserting
        """
        if limit is not None:
            new.extend(
                subtree.autocomplete(prefix, limit - len(new)))
        else:
            new.extend(
                subtree.autocomplete(prefix, limit))

    def _simple_remove_help(self)-> None:
        """
        update weights when inserting
        """
        if self.weight_type == 'sum':
            self.weight = 0.0
            for tree in self.subtrees:
                self.weight += tree.weight
        else:
            if self.__len__() == 0.0:
                self.weight = 0.0
            else:
                acc = 0
                for tree in self.subtrees:
                    acc += tree.weight * tree.__len__()
                self.weight = acc / self.__len__()
        for tree in self.subtrees:
            if tree.weight == 0:
                self.subtrees.remove(tree)

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        if self.weight == 0:
            pass
        elif self.value == prefix:
            self.subtrees = []
            self.weight = 0.0
        else:
            for subtree in self.subtrees:
                if len(subtree.value) <= len(prefix):
                    if subtree.value == prefix[:len(subtree.value)]:
                        subtree.remove(prefix)
                        self._simple_remove_help()

                elif len(subtree.value) > len(prefix):
                    if subtree.value[:len(prefix)] == prefix:
                        subtree.remove(prefix)
                        self._simple_remove_help()
            self.subtrees.sort(key=lambda x: x.weight, reverse=True)


################################################################################
# CompressedPrefixTree (Task 6)
################################################################################
class CompressedPrefixTree(Autocompleter):
    """A compressed prefix tree implementation.

    While this class has the same public interface as SimplePrefixTree,
    (including the initializer!) this version follows the implementation
    described on Task 6 of the assignment handout, which reduces the number of
    tree objects used to store values in the tree.

    === Attributes ===
    value:
        The value stored at the root of this prefix tree, or [] if this
        prefix tree is empty.
    weight:
        The weight of this prefix tree. If this tree is a leaf, this attribute
        stores the weight of the value stored in the leaf. If this tree is
        not a leaf and non-empty, this attribute stores the *aggregate weight*
        of the leaf weights in this tree.
    subtrees:
        A list of subtrees of this prefix tree.
    weight_type:
        Type of aggregate weight; either sum or average

    === Representation invariants ===
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0, then self.value == [] and self.subtrees == [].
        This represents an empty simple prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, this tree is a leaf.
        (self.value is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If len(self.subtrees) > 0, then self.value is a list (*common prefix*),
        and self.weight > 0 (*aggregate weight*).

    - **NEW**
      This tree does not contain any compressible internal values.
      (See the assignment handout for a definition of "compressible".)

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of their weights.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a `weight`
      attribute.
    """
    value: Optional[Any]
    weight: float
    subtrees: List[CompressedPrefixTree]
    weight_type: str

    def __init__(self, weight_type: str) -> None:
        """Initialize an empty simple prefix tree.

        Precondition: weight_type == 'sum' or weight_type == 'average'.

        The given <weight_type> value specifies how the aggregate weight
        of non-leaf trees should be calculated (see the assignment handout
        for details).
        """
        self.weight_type = weight_type
        self.weight = 0.0
        self.subtrees = []
        self.value = []

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        return self.weight == 0.0

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        return self.weight > 0 and self.subtrees == []

    def __str__(self) -> str:
        """Return a string representation of this tree.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.value} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        if self.weight == 0:
            return 0
        elif self.subtrees == [] and self.weight > 0:
            return 1
        else:
            length = 0
            for subtree in self.subtrees:
                length += subtree.__len__()
            return length

    def _comp_helper(self, value: Any, weight: float, prefix: List,
                     self_check: int) -> None:
        """
        helper for compressed insert
        """
        new = CompressedPrefixTree(self.weight_type)
        new.value = prefix
        new.weight = weight
        value_tree = CompressedPrefixTree(self.weight_type)
        value_tree.value = value
        value_tree.weight = weight
        new.subtrees.append(value_tree)
        existing = CompressedPrefixTree(self.weight_type)
        existing.value = self.value
        existing.weight = self.weight
        existing.subtrees = self.subtrees
        self.value = prefix[:self_check]
        self.subtrees = []
        self.subtrees.append(new)
        self.subtrees.append(existing)
        self.subtrees.sort(key=lambda x: x.weight, reverse=True)

    def _comp_helper2(self, value: Any, weight: float) -> None:
        """
        helper for compressed insert
        """
        new = CompressedPrefixTree(self.weight_type)
        new.value = value
        new.weight = weight
        value_tree = CompressedPrefixTree(self.weight_type)
        value_tree.value = self.value
        value_tree.weight = self.weight
        value_tree.subtrees = self.subtrees
        self.value = []
        self.subtrees = []
        self.subtrees.append(new)
        self.subtrees.append(value_tree)
        self.subtrees.sort(key=lambda x: x.weight, reverse=True)

    def _comp_helper3(self, value: Any, weight: float, prefix: List) -> None:
        """
        helper for compressed insert
        """
        new = CompressedPrefixTree(self.weight_type)
        new.value = prefix
        new.weight = weight
        value_tree = CompressedPrefixTree(self.weight_type)
        value_tree.value = value
        value_tree.weight = weight
        new.subtrees.append(value_tree)
        existing = CompressedPrefixTree(self.weight_type)
        existing.value = self.value
        existing.weight = self.weight
        existing.subtrees = self.subtrees
        self.value = []
        self.subtrees = []
        self.subtrees.append(new)
        self.subtrees.append(existing)
        self.subtrees.sort(key=lambda x: x.weight, reverse=True)

    def _comp_helper4(self, value: Any, prefix: List) -> int:
        """
        helper for compressed insert
        """
        matching = []
        for subtree in self.subtrees:
            if subtree.value == value:
                matching = [len(prefix) + 1]
                break
            else:
                count = 0
                for i in range(min(len(prefix), len(subtree.value))):
                    if subtree.value[i] == prefix[i] and not \
                            subtree.is_leaf():
                        count += 1
                    elif subtree.value[i] != prefix[i]:
                        break
                matching.append(count)
        return max(matching)

    def _comp_helper5(self, prefix: List) -> int:
        """
        helper for compressed insert
        """
        self_check = 0
        for i in range(min(len(self.value), len(prefix))):
            if self.value[i] == prefix[i]:
                self_check += 1
            else:
                break
        return self_check

    def _comp_helper6(self, value: Any, weight: float, prefix: List) -> None:
        """
        helper for compressed insert
        """
        self.value = prefix
        self.weight = weight
        value_tree = CompressedPrefixTree(self.weight_type)
        value_tree.value = value
        value_tree.weight = weight
        self.subtrees.append(value_tree)

    def _comp_helper7(self, value: Any, weight: float, prefix: List) -> None:
        """
        helper for compressed insert
        """

        new = CompressedPrefixTree(self.weight_type)
        new.weight = weight
        new.value = prefix
        value_tree = CompressedPrefixTree(self.weight_type)
        value_tree.weight = weight
        value_tree.value = value
        new.subtrees.append(value_tree)
        self.subtrees.append(new)
        self.subtrees.sort(key=lambda x: x.weight, reverse=True)

    def _comp_helper8(self, value: Any, weight: float, prefix: List) -> None:
        """
        helper for compressed insert
        """
        new = CompressedPrefixTree(self.weight_type)
        new.weight = weight
        new.value = prefix
        value_tree = CompressedPrefixTree(
            self.weight_type)
        value_tree.weight = weight
        value_tree.value = value
        new.subtrees.append(value_tree)
        self.subtrees.append(new)
        self.subtrees.sort(key=lambda x: x.weight, reverse=True)

    def _comp_helper9(self, value: Any, weight: float, prefix: List,
                      subtree: CompressedPrefixTree) -> None:
        """
        helper for compressed insert
        """
        new = CompressedPrefixTree(self.weight_type)
        new.weight = weight
        new.value = value
        merged = CompressedPrefixTree(self.weight_type)
        merged.value = prefix
        merged.subtrees.append(new)
        merged.subtrees.append(subtree)
        if self.weight_type == 'sum':
            for tree in merged.subtrees:
                merged.weight += tree.weight
        elif self.weight_type == 'average':
            acc = 0
            length = 0
            for tree in merged.subtrees:
                a = tree.__len__()
                length += a
                acc += tree.weight * a
            merged.weight = acc / length

        merged.subtrees.sort(key=lambda x: x.weight,
                             reverse=True)
        self.subtrees.append(merged)
        self.subtrees.remove(subtree)
        self.subtrees.sort(key=lambda x: x.weight,
                           reverse=True)

    def _comp_helper10(self, value: Any, weight: float, prefix: List) -> None:
        """
        helper for compressed insert
        """
        new = CompressedPrefixTree(self.weight_type)
        new.weight = weight
        new.value = prefix
        value_tree = CompressedPrefixTree(
            self.weight_type)
        value_tree.weight = weight
        value_tree.value = value
        new.subtrees.append(value_tree)
        self.subtrees.append(new)
        self.subtrees.sort(key=lambda x: x.weight,
                           reverse=True)

    def _comp_helper11(self) -> None:
        """
        update weights
        """
        if self.weight_type == 'sum':
            sum_weight = 0
            for subtree in self.subtrees:
                sum_weight += subtree.weight
            self.weight = sum_weight
        elif self.weight_type == 'average':
            acc = 0
            for tree in self.subtrees:
                acc += tree.weight * tree.__len__()
            self.weight = acc / self.__len__()

    def _comp_helper12(self, merged: CompressedPrefixTree) -> None:
        """
        update weights
        """
        if self.weight_type == 'sum':
            for tree in merged.subtrees:
                merged.weight += tree.weight
        elif self.weight_type == 'average':
            acc = 0
            length = 0
            for tree in merged.subtrees:
                a = tree.__len__()
                length += a
                acc += tree.weight * a
            merged.weight = acc / length

    def _comp_helper13(self, value: Any, weight: float, prefix: List,
                       acc: int) -> None:
        """
        Helper for compressed.insert()
        """
        for subtree in self.subtrees:
            if subtree.value == value:
                subtree.weight += weight
                break
            elif subtree.value[:acc] == prefix[:acc] and \
                    len(prefix) >= len(subtree.value):
                self_check = 0
                for i in range(min(len(self.value), len(prefix))):
                    if self.value[i] == prefix[i]:
                        self_check += 1
                    else:
                        break
                if self_check != acc:
                    subtree.insert(value, weight, prefix)
                    break
                elif self_check == acc:
                    self._comp_helper8(value, weight, prefix)
                    break
            elif subtree.value[:acc] == prefix[:acc] and not \
                    len(prefix) >= len(subtree.value):
                self_check = 0
                for i in range(min(len(self.value), len(prefix))):
                    if self.value[i] == prefix[i]:
                        self_check += 1
                    else:
                        break
                if len(prefix) == acc:
                    self._comp_helper9(value, weight, prefix,
                                       subtree)
                    break
                elif self_check == acc:
                    self._comp_helper10(value, weight, prefix)
                    break
                else:
                    new = CompressedPrefixTree(self.weight_type)
                    new.weight = weight
                    new.value = prefix
                    value_tree = CompressedPrefixTree(self.weight_type)
                    value_tree.weight = weight
                    value_tree.value = value
                    new.subtrees.append(value_tree)
                    merged = CompressedPrefixTree(self.weight_type)
                    merged.value = prefix[:acc]
                    merged.subtrees.append(new)
                    merged.subtrees.append(subtree)

                    self._comp_helper12(merged)

                    merged.subtrees.sort(key=lambda x: x.weight,
                                         reverse=True)
                    self.subtrees.append(merged)
                    self.subtrees.remove(subtree)
                    self.subtrees.sort(key=lambda x: x.weight,
                                       reverse=True)
                    break

    def insert(self, value: Any, weight: float, prefix: List) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this prefix tree
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
            weight > 0
            The given value is either:
                1) not in this Autocompleter
                2) was previously inserted with the SAME prefix sequence
        """
        if self.weight == 0.0:
            self._comp_helper6(value, weight, prefix)
        else:
            acc = self._comp_helper4(value, prefix)
            if acc == 0:
                if prefix == [] and self.value == []:
                    new = CompressedPrefixTree(self.weight_type)
                    new.weight = weight
                    new.value = value
                    self.subtrees.append(new)
                    self.subtrees.sort(key=lambda x: x.weight, reverse=True)
                elif not self.value == []:
                    self_check = self._comp_helper5(prefix)
                    if self_check > 0:
                        self._comp_helper(value, weight, prefix, self_check)
                    elif not prefix != []:
                        self._comp_helper2(value, weight)
                    else:
                        self._comp_helper3(value, weight, prefix)
                else:
                    self._comp_helper7(value, weight, prefix)
            else:
                self._comp_helper13(value, weight, prefix, acc)
            # updates weights
            self._comp_helper11()

    def autocomplete(self, prefix: List,
                     limit: Optional[int] = None) -> List[Tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Precondition: limit is None or limit > 0.
        """
        new = []
        if self.weight == 0:
            return []
        else:
            for subtree in self.subtrees:
                if len(new) == limit:
                    break
                elif subtree.is_leaf() and self.value[:len(prefix)] == prefix:
                    new.append((subtree.value, subtree.weight,))
                elif subtree.value == prefix[:len(subtree.value)]:
                    if limit is not None:
                        new.extend(subtree.autocomplete(prefix,
                                                        limit - len(new)))
                    else:
                        new.extend(
                            subtree.autocomplete(prefix, limit))
                elif len(prefix) < len(subtree.value):
                    if subtree.value[:len(prefix)] == prefix:
                        self._auto_help(new, prefix, subtree, limit)

        new.sort(key=lambda x: x[1], reverse=True)
        return new

    @staticmethod
    def _auto_help(new: List, prefix: List, subtree: 'CompressedPrefixTree',
                   limit: Optional[int] = None) -> None:
        """
        helper for compressed.autocomplete()
        """
        if limit is not None:
            new.extend(
                subtree.autocomplete(prefix, limit - len(new)))
        else:
            new.extend(
                subtree.autocomplete(prefix, limit))

    def remove(self, prefix: List) -> None:
        """Remove all values that match the given prefix.
        """
        if self.weight == 0:
            pass
        elif self.value == prefix:
            self.subtrees = []
            self.weight = 0.0
        else:
            for subtree in self.subtrees:
                if len(subtree.value) < len(prefix) and subtree.value == \
                        prefix[:len(subtree.value)]:
                    subtree.remove(prefix)

                    # update weights
                    self._helper()

                elif len(subtree.value) >= len(prefix) and \
                        subtree.value[:len(prefix)] == prefix:
                    if not self.value != []:
                        subtree.weight = 0.0
                    elif len(self.subtrees) == 2:
                        self.subtrees.remove(subtree)
                        tree = self.subtrees[0]
                        self.value = tree.value
                        self.subtrees.extend(tree.subtrees)
                        self.subtrees = self.subtrees[1:]
                    elif len(self.subtrees) > 2:
                        self.subtrees.remove(subtree)

                    self._helper()
            self.subtrees.sort(key=lambda x: x.weight, reverse=True)

    def _helper(self) -> None:
        """
        updates weights of self after removal
        """

        if self.weight_type == 'sum':
            self.weight = 0.0
            for tree in self.subtrees:
                self.weight += tree.weight
        else:
            if self.__len__() == 0.0:
                self.weight = 0.0
            else:
                acc = 0
                for tree in self.subtrees:
                    acc += tree.weight * tree.__len__()
                self.weight = acc / self.__len__()
        for tree in self.subtrees:
            if tree.weight == 0:
                self.subtrees.remove(tree)


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'max-nested-blocks': 4
    })
