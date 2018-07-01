import inspect

import numpy as np
import pandas as pd

from graphviz import Digraph


class ClassSpy(object):
    def __init__(self):
        self.__dict__["sets"] = []
        self.__dict__["gets"] = []

    def __setattr__(self, key, value):
        caller = inspect.currentframe().f_back
        if (type(value) == np.ndarray):
            self.sets.append([key, type(value).__name__ + str(value.shape), caller.f_code.co_filename.split("\\")[-1],
                              caller.f_lineno])
            self.__dict__[key] = ArraySpy(value, key, self.__dict__["gets"], self.__dict__["sets"])
        elif (type(value) != int and type(value) != np.float64 and type(value) != float):
            print(type(value))  # just in case this type would need a custom method like numpy arrays
            self.sets.append([key, type(value).__name__, caller.f_code.co_filename.split("\\")[-1], caller.f_lineno])
            self.__dict__[key] = value
        else:
            self.sets.append([key, type(value).__name__, caller.f_code.co_filename.split("\\")[-1], caller.f_lineno])
            self.__dict__[key] = value

    def __getattribute__(self, item):
        if (item != "__dict__" and item != "sets" and item != "gets" and item != "save_connections"):
            caller = inspect.currentframe().f_back
            object.__getattribute__(self, "gets").append(
                [item, caller.f_code.co_filename.split("\\")[-1], str(caller.f_lineno)])
            return object.__getattribute__(self, item)
        else:
            return object.__getattribute__(self, item)

    def plot(self,variable_subset=None):
        dot = Digraph(comment='Class Spy generated Graph', strict=True, engine="dot")
        # splines="true"
        # overlap_scaling = '10'
        dot.attr(overlap="scale", rankdir='LR', size='180,180')
        dot.attr('node', color="#000000", style='solid')
        dot.attr('node', shape='box')
        # dot.format = 'svg'
        variable_edges = pd.read_csv("connections.csv")

        complete_edges = variable_edges[
            variable_edges['Variable_set'].notnull() & variable_edges['Variable_get'].notnull()]
        for index, row in complete_edges.iterrows():
            # with dot.subgraph(name=key, node_attr={'shape': 'box'},body="test") as c:
#             if (type(
#                     variable_subset) == list):  # add the edge if it is in the subset, or if we weren't passed a subset
#                 if (row[0] not in variable_subset or row[4] not in variable_subset):
#                     continue

            dot.node(row[0])
            dot.node(row[4])
            dot.edge(row[4], row[0])

        #dot.save('graph.dot')
        dot.render('Classspy.gv', view=True)

    def save_connections(self):
        sets = pd.DataFrame(self.sets,columns=["Variable","Type","File","LineNo"],dtype="str")
        gets = pd.DataFrame(self.gets,columns=["Variable","File","LineNo"],dtype="str")
        sets.drop_duplicates()
        gets.drop_duplicates()
        # write edge connection csv
        variable_edges = pd.merge(sets, gets, how='outer', on=("LineNo", "File"), suffixes=('_set', '_get'))
        variable_edges.to_csv("connections.csv", index=False)
        return variable_edges


class ArraySpy(np.ndarray):
    def __new__(cls, input_array, name, gets_in, sets_in):
        obj = np.asarray(input_array).view(cls)
        obj.name = name
        obj.gets = gets_in
        obj.sets = sets_in
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        self.info = getattr(obj, 'info', None)

    def __getitem__(self, item):
        # print(self.name + "[" + str(item) + "]")
        attr = np.ndarray.__getitem__(self, item)
        if issubclass(type(attr), np.ndarray):  # handle multi dimensional arrays
            return ArraySpy(attr, self.name, self.gets, self.sets)
        else:
            caller = inspect.currentframe().f_back
            object.__getattribute__(self, "gets").append(
                [self.name, caller.f_code.co_filename.split("\\")[-1], str(caller.f_lineno)])
            return attr

    def __setitem__(self, key, value):
        # print(self.name,value)
        caller = inspect.currentframe().f_back
        self.sets.append(
            [self.name, type(value).__name__, caller.f_code.co_filename.split("\\")[-1], caller.f_lineno])
        np.ndarray.__setitem__(self, key, value)
