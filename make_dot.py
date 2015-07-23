"""
A tool to create a bigraph of spf lookups.
Copyright (C) 2015 Robert Corsaro

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from dns.resolver import query

def find(predicate, itr):
    """
    find first node that matches predicate
    """
    def a(a, i):
        return a or f(i) and i or None
    return reduce(a, itr)


class Node(object):
    """
    Node for resolve message tree
    """
    def __init__(self, name):
        self.name = name
        self.children_names = set()
        self.children = []

    def add_child(self, name):
        if name not in self.children_names:
            node = Node(name)
            self.children.append(node)
            return node
        else:
            return find(lambda x: x.name == name, self.children)

    def __unicode__(self):
        return "{} -> ({})".format(self.name, ', '.join(map(unicode, self.children)))

    def __str__(self):
        return self.__unicode__()


class TreeBuilder(object):
    """
    Builds Node tree from resolve messages
    """
    def __init__(self):
        self.stack = []
        self.resolver = Resolver()

    def build(self, domain):
        """
        Returns a tree of the spf lookups
        """
        tree = None
        for typ, name in self.resolver(domain):
            if typ == 'enter':
                if len(self.stack):
                    node = self.stack[-1].add_child(name)
                else:
                    node = Node(name)
                self.stack.append(node)
            elif typ == 'exit':
                tree = Tree(self.stack.pop())
        return tree


class Resolver(object):
    """
    Resolve spf records
    """

    @classmethod
    def is_include(cls, record):
        """
        is an include spf record?
        """
        return record.startswith('include:')

    def __call__(self, domain):
        """
        queries spf records on domain recursively, sending messages to caller
        as it enters and exits each DNS record.
        """
        yield 'enter', domain
        res = map(lambda x: x.to_text(), query(domain, "TXT"))
        terms = find(lambda x: x.startswith('v=spf1'), res).split()
        for record in filter(self.is_include, terms):
            name = record.split(':')[1]
            for typ, name in self(name):
                yield typ, name

        yield 'exit', domain


class Tree(object):
    """
    Tree of nodes
    """
    def __init__(self, head):
        self.head = head

    def bigrams(self, node=None):
        """
        generates bigrams for each relationship in the graph
        """
        if not node:
            node = self.head

        if not len(node.children):
            return
        else:
            for n in node.children:
                for bigram in self.bigrams(n):
                    yield bigram
                yield node.name, n.name

    def __unicode__(self):
        return unicode(self.head)

    def __str__(self):
        return self.__unicode__()


def main(domain):
    print 'digraph G {'
    for a, b in TreeBuilder().build(domain).bigrams():
        print '    "{}" -> "{}"'.format(a, b)
    print '}'

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        "ERROR: Takes one argument that is domain name"
        sys.exit(1)

    main(sys.argv[1])