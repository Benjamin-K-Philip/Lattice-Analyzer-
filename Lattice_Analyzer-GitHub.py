import networkx as nx
import matplotlib.pyplot as plt


class LatticeAnalyzer:
    def __init__(self):
        self.relation = set()
        self.elements = set()

    def parse_relation(self, relation_input):
        """Parse relation input like: (1,2) (2,3) (1,3)"""
        try:
            pairs = relation_input.strip().split()
            self.relation = set()
            self.elements = set()

            for pair in pairs:
                if not (pair.startswith('(') and pair.endswith(')')):
                    raise ValueError(f"Invalid format: {pair}. Use (a,b) format")

                pair = pair[1:-1]
                parts = pair.split(',')

                if len(parts) != 2:
                    raise ValueError(f"Each pair must have exactly 2 elements: {pair}")

                try:
                    a, b = int(parts[0].strip()), int(parts[1].strip())
                    self.relation.add((a, b))
                    self.elements.add(a)
                    self.elements.add(b)
                except ValueError:
                    raise ValueError(f"Elements must be integers: {pair}")

            return True
        except Exception as e:
            print(f"Error parsing relation: {e}")
            return False

    def build_divisibility_relation_from_elements(self, elements_input):
        """
        Read elements like: 1 2 3 6
        Build relation a|b on that set (i.e., (a,b) in R iff a divides b).
        """
        try:
            parts = elements_input.strip().split()
            if not parts:
                raise ValueError("No elements provided")

            els = set()
            for p in parts:
                els.add(int(p))

            self.elements = els
            self.relation = set()
            for a in self.elements:
                for b in self.elements:
                    if b % a == 0:
                        self.relation.add((a, b))
            return True
        except Exception as e:
            print(f"Error parsing elements: {e}")
            return False

    def is_reflexive(self):
        return all((e, e) in self.relation for e in self.elements)

    def is_irreflexive(self):
        return all((e, e) not in self.relation for e in self.elements)

    def is_symmetric(self):
        return all((b, a) in self.relation for (a, b) in self.relation)

    def is_antisymmetric(self):
        for (a, b) in self.relation:
            if (b, a) in self.relation and a != b:
                return False
        return True

    def is_asymmetric(self):
        return all((b, a) not in self.relation for (a, b) in self.relation)

    def is_transitive(self):
        for (a, b) in self.relation:
            for (c, d) in self.relation:
                if b == c and (a, d) not in self.relation:
                    return False
        return True

    def get_properties(self):
        return {
            "Reflexive": self.is_reflexive(),
            "Irreflexive": self.is_irreflexive(),
            "Symmetric": self.is_symmetric(),
            "Antisymmetric": self.is_antisymmetric(),
            "Asymmetric": self.is_asymmetric(),
            "Transitive": self.is_transitive()
        }

    def get_transitive_closure(self):
        closure = set(self.relation)
        for k in self.elements:
            for i in self.elements:
                for j in self.elements:
                    if (i, k) in closure and (k, j) in closure:
                        closure.add((i, j))
        return closure

    def get_upper_bounds(self, elements):
        closure = self.get_transitive_closure()
        upper_bounds = set()
        for ub in self.elements:
            if all((e, ub) in closure for e in elements):
                upper_bounds.add(ub)
        return upper_bounds

    def get_lower_bounds(self, elements):
        closure = self.get_transitive_closure()
        lower_bounds = set()
        for lb in self.elements:
            if all((lb, e) in closure for e in elements):
                lower_bounds.add(lb)
        return lower_bounds

    def get_minimal_elements(self):
        closure = self.get_transitive_closure()
        minimal = set()
        for e in self.elements:
            is_minimal = True
            for other in self.elements:
                if other != e and (other, e) in closure:
                    is_minimal = False
                    break
            if is_minimal:
                minimal.add(e)
        return minimal

    def get_maximal_elements(self):
        closure = self.get_transitive_closure()
        maximal = set()
        for e in self.elements:
            is_maximal = True
            for other in self.elements:
                if other != e and (e, other) in closure:
                    is_maximal = False
                    break
            if is_maximal:
                maximal.add(e)
        return maximal

    def get_least_element(self):
        lower = self.get_lower_bounds(self.elements)
        return min(lower) if lower else None

    def get_greatest_element(self):
        upper = self.get_upper_bounds(self.elements)
        return max(upper) if upper else None

    def get_glb(self, elements):
        lower = self.get_lower_bounds(elements)
        return max(lower) if lower else None

    def get_lub(self, elements):
        upper = self.get_upper_bounds(elements)
        return min(upper) if upper else None

    def is_join_semilattice(self):
        from itertools import combinations
        for pair in combinations(self.elements, 2):
            if self.get_lub(pair) is None:
                return False
        return True

    def is_meet_semilattice(self):
        from itertools import combinations
        for pair in combinations(self.elements, 2):
            if self.get_glb(pair) is None:
                return False
        return True

    def is_lattice(self):
        return self.is_join_semilattice() and self.is_meet_semilattice()

    def classify_lattice(self):
        if self.is_lattice():
            return "LATTICE"
        elif self.is_join_semilattice():
            return "JOIN SEMILATTICE"
        elif self.is_meet_semilattice():
            return "MEET SEMILATTICE"
        else:
            return "NOT A LATTICE"

    def get_cover_relations(self):
        closure = self.get_transitive_closure()
        covered = set()
        for (a, b) in closure:
            if a == b:
                continue
            is_covering = True
            for c in self.elements:
                if c != a and c != b and (a, c) in closure and (c, b) in closure:
                    is_covering = False
                    break
            if is_covering:
                covered.add((a, b))
        return covered

    def draw_hasse_diagram_graph(self):
        try:
            if not self.elements:
                print("No elements to draw.")
                return

            # Build cover graph
            covers = self.get_cover_relations()
            G = nx.DiGraph()
            G.add_nodes_from(self.elements)
            G.add_edges_from(covers)

            # Compute levels: 0 = minimal elements, larger = higher in poset
            closure = self.get_transitive_closure()
            minimal = self.get_minimal_elements()

            # BFS-like layering from minimal elements
            level = {e: None for e in self.elements}
            frontier = list(minimal)
            for e in frontier:
                level[e] = 0

            while frontier:
                new_frontier = []
                for u in frontier:
                    for v in self.elements:
                        # u covers v? (u < v and no w with u < w < v)
                        if (u, v) in covers and level[v] is None:
                            level[v] = level[u] + 1
                            new_frontier.append(v)
                frontier = new_frontier

            # If some nodes were not reached (isolated or cycles), put them at level 0
            for e in self.elements:
                if level[e] is None:
                    level[e] = 0

            # Group by level
            levels = {}
            for node, lev in level.items():
                levels.setdefault(lev, []).append(node)

            # Assign positions: x spread within each level, y = level (minimal at bottom)
            pos = {}
            max_level = max(level.values()) if level else 0
            for lev, nodes_at_level in levels.items():
                nodes_at_level = sorted(nodes_at_level)
                n = len(nodes_at_level)
                # spread x from -1 to 1
                if n == 1:
                    xs = [0.0]
                else:
                    xs = [ -1.0 + 2.0 * i / (n - 1) for i in range(n) ]
                # y: minimal level at bottom -> use lev directly (or -lev if you prefer)
                for x, node in zip(xs, nodes_at_level):
                    pos[node] = (x, lev)

            plt.figure(figsize=(6, 6))
            nx.draw(
                G,
                pos,
                with_labels=True,
                node_color="lightblue",
                node_size=800,
                arrows=True,
                arrowstyle="->",
                arrowsize=15,
                font_size=10
            )
            plt.title("Hasse Diagram (least at bottom, greatest at top)")
            plt.axis("off")
            plt.show()
        except Exception as e:
            print(f"Error drawing Hasse diagram: {e}")

    def display_lattice_analysis(self):
        print("\n" + "="*60) # to print = 60 times
        print("HASSE DIAGRAM & LATTICE ANALYSIS (Divisibility)")
        print("="*60)

        print(f"\nElements: {sorted(self.elements)}")
        print(f"Relation (a divides b): {sorted(self.relation)}")

        print("\n" + "-"*60)  # to print - 60 times
        print("LATTICE ELEMENTS:")
        print("-"*60)
        print(f"Minimal Elements: {sorted(self.get_minimal_elements())}")
        print(f"Maximal Elements: {sorted(self.get_maximal_elements())}")
        print(f"Least Element: {self.get_least_element()}")
        print(f"Greatest Element: {self.get_greatest_element()}")

        print("\n" + "-"*60)
        print("BOUNDS FOR ALL ELEMENTS:")
        print("-"*60)
        print(f"Upper Bounds: {sorted(self.get_upper_bounds(self.elements))}")
        print(f"Lower Bounds: {sorted(self.get_lower_bounds(self.elements))}")
        print(f"Greatest Lower Bound(GLB ): {self.get_glb(self.elements)}")
        print(f"Least Upper Bound (LUB): {self.get_lub(self.elements)}")

        print("\n" + "-"*60)
        print("LATTICE CLASSIFICATION:")
        print("-"*60)
        print(f"{self.classify_lattice()}")

        print("\n" + "="*60)
        self.draw_hasse_diagram_graph()

    def display_relation_properties(self):
        print("\n" + "="*60)
        print("RELATION PROPERTIES CHECK")
        print("="*60)

        print(f"\nElements: {sorted(self.elements)}")
        print(f"Relation: {sorted(self.relation)}")

        print("\n" + "-"*60)
        print("PROPERTIES:")
        print("-"*60)
        properties = self.get_properties()
        for prop, value in properties.items():
            print(f"{prop}: {value}")
        print("\n" + "="*60)


class ExpressionTree:
    def __init__(self):
        self.tree = None
        self.node_counter = 0

    def parse_expression(self, expr):
        """Parse expression like: (1+2)*3 into tree"""
        try:
            expr = expr.replace(" ", "")
            valid_chars = set("0123456789+-*/()")
            if not all(c in valid_chars for c in expr):
                raise ValueError("Invalid characters in expression")

            self.tree, pos = self._parse_expr(expr, 0)
            if self.tree is None or pos != len(expr):
                raise ValueError("Failed to parse entire expression")
            return True
        except Exception as e:
            print(f"Error parsing expression: {e}")
            return False

    def _parse_expr(self, expr, pos):
        left, pos = self._parse_term(expr, pos)
        if left is None:
            return None, pos

        while pos < len(expr) and expr[pos] in ['+', '-']:
            op = expr[pos]
            pos += 1
            right, pos = self._parse_term(expr, pos)
            if right is None:
                raise ValueError(f"Expected term after operator {op}")
            left = {'op': op, 'left': left, 'right': right}

        return left, pos

    def _parse_term(self, expr, pos):
        left, pos = self._parse_factor(expr, pos)
        if left is None:
            return None, pos

        while pos < len(expr) and expr[pos] in ['*', '/']:
            op = expr[pos]
            pos += 1
            right, pos = self._parse_factor(expr, pos)
            if right is None:
                raise ValueError(f"Expected factor after operator {op}")
            left = {'op': op, 'left': left, 'right': right}

        return left, pos

    def _parse_factor(self, expr, pos):
        if pos >= len(expr):
            return None, pos

        if expr[pos] == '(':
            pos += 1
            result, pos = self._parse_expr(expr, pos)
            if pos >= len(expr) or expr[pos] != ')':
                raise ValueError("Missing closing parenthesis")
            pos += 1
            return result, pos

        if expr[pos].isdigit():
            num = ""
            while pos < len(expr) and expr[pos].isdigit():
                num += expr[pos]
                pos += 1
            return {'value': int(num), 'left': None, 'right': None}, pos

        return None, pos

    def _collect_graph_nodes(self, node, G, parent_id=None):
        """Collect nodes and edges into a networkx graph (parent -> child)"""
        if node is None:
            return

        node_id = self.node_counter
        self.node_counter += 1

        label = str(node.get('op', node.get('value', '?')))
        G.add_node(node_id, label=label)

        if parent_id is not None:
            G.add_edge(parent_id, node_id)

        if node.get('left'):
            self._collect_graph_nodes(node['left'], G, node_id)
        if node.get('right'):
            self._collect_graph_nodes(node['right'], G, node_id)

    def _assign_positions(self, node, depth=0, x=0.0, dx=1.0, pos=None, idx=None):
        """
        Recursively assign positions so that:
        - parent is above children,
        - left child is to the left, right child to the right.
        """
        if node is None:
            return

        if pos is None:
            pos = {}
        if idx is None:
            idx = {'id': 0, 'map': {}}

        node_key = id(node)
        if node_key not in idx['map']:
            idx['map'][node_key] = idx['id']
            idx['id'] += 1
        node_id = idx['map'][node_key]

        pos[node_id] = (x, -depth)

        left = node.get('left')
        right = node.get('right')

        if left:
            self._assign_positions(left, depth + 1, x - dx, dx / 2, pos, idx)
        if right:
            self._assign_positions(right, depth + 1, x + dx, dx / 2, pos, idx)

        return pos, idx['map']

    def draw_tree_graph(self):
        """Draw expression tree as graph using networkx and direction-specific layout"""
        try:
            if self.tree is None:
                print("No expression tree to draw")
                return

            G = nx.DiGraph()
            self.node_counter = 0
            self._collect_graph_nodes(self.tree, G, None)
            labels = nx.get_node_attributes(G, 'label')

            pos, id_map = self._assign_positions(self.tree, depth=0, x=0.0, dx=1.0)

            mapping = {}
            nodes_list = list(G.nodes())
            dict_nodes = list(id_map.items())
            dict_nodes.sort(key=lambda kv: kv[1])
            for i, (node_key, small_id) in enumerate(dict_nodes):
                mapping[small_id] = nodes_list[i]

            graph_pos = {}
            for small_id, (x, y) in pos.items():
                graph_pos[mapping[small_id]] = (x, y)

            plt.figure(figsize=(8, 6))
            nx.draw(
                G,
                graph_pos,
                labels=labels,
                with_labels=True,
                node_color="lightgreen",
                node_size=800,
                arrows=True,
                arrowstyle="->",
                arrowsize=15,
                font_size=10
            )
            plt.title("Expression Tree (direction-specific)")
            plt.axis("off")
            plt.show()
        except Exception as e:
            print(f"Error drawing expression tree: {e}")


def main():
    print("\n" + "="*60)
    print("LATTICE & EXPRESSION TREE ANALYZER")
    print("="*60)

    while True:
        print("\nSelect an option:")
        print("1. Check relation properties (Reflexive, Symmetric, Transitive, Irreflexive, Antisymmetic, Asymmetirc.)")
        print("2. Hasse Diagram & Lattice Analysis (from elements, using divisibility)")
        print("3. Draw Expression Tree")
        print("4. Exit")

        choice = input("\nEnter your choice (1/2/3/4): ").strip()

        if choice == '1':
            print("\n" + "-"*60)
            print("RELATION PROPERTIES CHECK")
            print("-"*60)
            print("Enter relation as: (a,b) (c,d) (e,f) ...")
            print("Example: (1,1) (1,2) (2,2) (2,3) (3,3)")

            relation_input = input("\nEnter relation: ").strip()

            if not relation_input:
                print("No input provided")
                continue

            analyzer = LatticeAnalyzer()
            if analyzer.parse_relation(relation_input):
                analyzer.display_relation_properties()

        elif choice == '2':
            print("\n" + "-"*60)
            print("HASSE DIAGRAM & LATTICE ANALYSIS (Divisibility Relation)")
            print("-"*60)
            print("Enter elements (space-separated):")
            print("Example: 1 2 4 8")

            elements_input = input("\nEnter elements: ").strip()

            if not elements_input:
                print("No input provided")
                continue

            analyzer = LatticeAnalyzer()
            if analyzer.build_divisibility_relation_from_elements(elements_input):
                analyzer.display_lattice_analysis()

        elif choice == '3':
            print("\n" + "-"*60)
            print("EXPRESSION TREE BUILDER")
            print("-"*60)
            print("Enter expression with operators: + - * /")
            print("Example: (1+2)*3, 5*(2+3), (2+3)*4, (3+2)*(4-2), etc.")
            print("Minimum 2 operands required")

            expr_input = input("\nEnter expression: ").strip()

            if not expr_input:
                print("No input provided")
                continue

            import re
            operands = re.findall(r'\d+', expr_input)
            if len(operands) < 2:
                print("Expression must have at least 2 operands")
                continue

            tree = ExpressionTree()
            if tree.parse_expression(expr_input):
                tree.draw_tree_graph()

        elif choice == '4':
            print("\nThank you. Exiting Program")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
