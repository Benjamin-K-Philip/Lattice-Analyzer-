# Lattice Analyzer

# Description
A Python-based console application that analyzes mathematical relations, evaluates lattice structures, and visualizes algebraic expression trees. It leverages Object-Oriented Programming (OOP) concepts, graph theory algorithms, and data visualization libraries like networkx and matplotlib to provide a practical, interactive mathematical tool.

---

## How the Code Works

The Lattice & Expression Tree Analyzer is designed using modular Object-Oriented Programming (OOP) principles in Python. The code is organized into specific classes to handle core logic, mathematical modeling, and graph visualization.

➤ **Core Architecture and Modules** <br>
The application is divided into logical components that manage different mathematical operations:

   - **Main Module:** The main() function serves as the interactive console loop, handling user input, validating choices, and instantiating the appropriate objects based on the user's selected operation.

   - **LatticeAnalyzer Class:** Handles the parsing of mathematical relations and elements. It maintains the internal state of the relation and elements as sets, evaluating discrete math properties and building graphs.

   - **ExpressionTree Class:** Acts as a recursive descent parser. It takes string-based algebraic expressions and converts them into a hierarchical binary tree data structure, managing node counters and graph mappings.


➤ **Core Logic and Execution Flow** <br>
The main logic depends on the user's chosen path from the command line interface:

   - **Relation Properties:** The system parses pairs like (1,2) into a set of tuples. It then runs boolean checks iterating through the sets to determine properties like reflexivity, symmetry, transitivity, and antisymmetry.

   - **Lattice Analysis & Hasse Diagrams:** When a user inputs a set of integers, the system automatically builds a divisibility relation (where a divides b). It calculates the transitive closure to find covering relations, determines upper/lower bounds (LUB, GLB), and classifies the set as a Lattice or Semilattice. For the Hasse Diagram, it uses a Breadth-First Search (BFS) approach to assign hierarchical levels to elements, placing minimal elements at the bottom and greatest at the top before rendering the graph.

   - **Expression Parsing:** The expression tree evaluates a string like (1+2)*3 by respecting the order of operations (parentheses, multiplication/division, addition/subtraction). It recursively builds left and right child nodes for operators and uses custom coordinate mapping (_assign_positions) to ensure the generated graph visually represents a proper top-down binary tree.


➤ **Implementation of OOP and Algorithmic Concepts** <br>
The code serves as a practical application of discrete mathematics and programmatic concepts:

   - **Encapsulation:** The internal sets (self.relation, self.elements, self.tree) are bound to their respective class instances. All modifications and evaluations are done through specific class methods.

   - **Recursion:** Heavily utilized in ExpressionTree for both parsing the mathematical string (_parse_expr, _parse_term) and for traversing the tree to build the NetworkX graph.

   - **Graph Theory:** Applies directed acyclic graphs (DAGs) to map mathematical hierarchies, computing transitive reductions (cover relations) to draw simplified, accurate Hasse diagrams.

   - **Exception Handling:** Uses try-except blocks and ValueError raises to catch malformed inputs (e.g., missing parentheses, non-integer elements, invalid relation syntax) to prevent application crashes and prompt the user gracefully.

---


## Features 
  - Parse and validate mathematical relations in standard (a,b) format.

  - Identify and output relation properties (Reflexive, Irreflexive, Symmetric, Antisymmetric, Asymmetric, Transitive).

  - Automatically generate divisibility relations from user-provided integer sets.

  - Determine lattice bounds including Minimal/Maximal elements, Least/Greatest elements, and Greatest Lower Bound (GLB) / Least Upper Bound (LUB).

  - Classify mathematical sets accurately (e.g., Lattice, Join Semilattice, Meet Semilattice, Not a Lattice).

  - Render visually hierarchical Hasse diagrams using Matplotlib and NetworkX.

  - Parse standard algebraic expressions with operator precedence into binary trees and visualize them as directed graphs.

---

## Project Sructure  <br>
While contained in a single Python script, the logical structure mimics a modular project:

  - **Command Line Interface:** This maps directly to the main() function, which uses the while True loop and input() statements to create an interactive menu for the user.

  - **LatticeAnalyzer:** This maps to the class LatticeAnalyzer: block, which houses all the logic for relations (is_reflexive, is_transitive, etc.) and bounds (get_lub, get_glb).

  - **ExpressionTree:** This maps to the class ExpressionTree: block, which contains the recursive parsing logic (_parse_expr, _parse_term) to break down the math strings.

  - **Visualization Engine:** This refers to the specific methods inside those classes (draw_hasse_diagram_graph and draw_tree_graph) that utilize the networkx (nx) and matplotlib.pyplot (plt) libraries to calculate node coordinates and draw the charts.
