import numpy as np

class BVHNode:
    def __init__(self, name):
        self.name = name
        self.property = {}

    def add_property(self, data):
        if not data:
            return
        if data[0].startswith("OFFSET"):
            self.property["offset"] = [float(v) for v in data[1:]]
        elif data[0].startswith("CHANNELS"):
            ## temp do noting
            self.property["channels"] = data[1:]
        else:
            raise NotImplementedError()

    def get_property(self, property_name):
        return self.property.get(property_name.lower(), None)

    def __str__(self):
        return f"{self.name}-[property]->{'-[property]->'.join(self.property.keys())}"




class BVHLoader:
    def __init__(self, path):
        self.nodes = []
        self.nodes_to_parent_id = []
        self.nodes_name_to_id = {}
        self.__do_io_read(path)


    def __do_io_read(self, path):
        raw_data = None
        with open(path, 'r') as f:
            raw_data = f.readlines()

        hierarchy_line = -1
        motion_line = -1
        for idx, line in enumerate(raw_data):
            if line.startswith("HIERARCHY"):
                hierarchy_line = idx
            if line.startswith("MOTION"):
                motion_line = idx
        assert(motion_line > hierarchy_line and hierarchy_line != -1 and motion_line != -1)
        self.__do_parse_hierarchy(raw_data[hierarchy_line + 1: motion_line])
        self.__do_parse_motion(raw_data[motion_line+1:])


    def __do_parse_hierarchy(self, raw_data):
        stark = []

        def do_add_node(name, token):
            new_node = BVHNode(name)
            self.nodes.append(new_node)
            index = len(self.nodes) -1
            self.nodes_name_to_id[name] = index
            assert(len(self.nodes_to_parent_id) == index)

            if not stark:
                self.nodes_to_parent_id.append(-1)
            else:
                self.nodes_to_parent_id.append(stark[-1])

        for line in raw_data:
            token = line.strip().split()

            if token[0].startswith("ROOT"):
                do_add_node('RootJoint', token)
            elif token[0].startswith("End"):
                do_add_node(self.nodes[stark[-1]].name+"_end", token)
            elif token[0].startswith("JOINT"):
                do_add_node(token[1], token)
            elif token[0].startswith("{"):
                stark.append(len(self.nodes)-1)
            elif token[0].startswith("}"):
                stark.pop(-1)
            else:
                node = self.nodes[stark[-1]]
                node.add_property(token)


    def __do_parse_motion(self, raw_data):
        pass

    def get_offset(self):
        return  [np.array(node.get_property("offset")) for node in self.nodes]

    def get_joint_names(self):
        return [v.name for v in self.nodes]

    def get_parents(self):
        return self.nodes_to_parent_id


if __name__ == "__main__":
    data = BVHLoader("./data/walk60.bvh")
    for node in data.nodes:
        print(node)
    print("===============================")
    print(data.nodes_name_to_id)
    print("===============================")
    print(data.nodes_to_parent_id)




