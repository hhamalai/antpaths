import os.path
import xml.etree.ElementTree

def process_files(graph_data, dirname, names):
    build_files =  [x for x in names if x.endswith(".xml") and not x.startswith(".")]
    for build_file in build_files:
        targets = {}
        target_elements = xml.etree.ElementTree.fromstring(file(build_file).read()).findall("target")
        for target in target_elements:
            target_name = target.attrib.get("name") or ""
            target_depends = target.attrib.get("depends")
            if target_depends is not None:
                target_depends = target_depends.split(",")
            else:
                target_depends = []
            targets[target_name] = target_depends

        graph_data[build_file] = targets

def output_graph(graphdef):
    of = file("ant-graph.dot", "w")
    of.write("digraph G {\n")
    filenames = graphdef.keys()
    
    for filename in filenames:
        targets = [x for x in graphdef[filename].keys()]
        of.write("\tsubgraph \"%s\" {\n\t" % filename)
        for target in targets:
            of.write("\"%s\"; " % target)
        of.write("\n\t")
        of.write("label = \"%s\"" % filename)
        of.write("\t}\n")
    for filename in filenames:
        targets = [x for x in graphdef[filename].keys()]
        for target in targets:
            deps = graphdef[filename][target]
            for dep in deps:
                of.write("\"%s\" -> \"%s\";\n" % (target, dep))
    of.write("}\n")
    of.close()


def main():
    graph_data = {}
    os.path.walk(".", process_files, graph_data)
    output_graph(graph_data)

if __name__ == '__main__':
    main()
