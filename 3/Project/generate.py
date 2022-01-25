import sys

from crossword import *

import time


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        #Remove all words that do not match the length of the variable
        for var in self.crossword.variables:
            #Make a copy of the set to iterate through
            words = self.domains[var].copy()
            for word in words:
                #Compare variable length to word length
                if(var.length != len(word)):
                    #Remove any offending elements from the original set
                    self.domains[var].remove(word)
        
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #Create a revision flag
        revised = False
        overlap = self.crossword.overlaps[x,y]
        if overlap:
            #Create a copy of the x domain to iterate through
            xDomain = self.domains[x].copy()
            for xWord in xDomain:
                #See if xWord conflicts with all words in y's domain
                conflict = True
                for yWord in self.domains[y]:
                    if (xWord[overlap[0]] == yWord[overlap[1]]):
                        conflict = False
                        break
                #If there is no possible configuration of xWord in y's domain
                if conflict: 
                    #Remove xWord from x's domain and update the revised flag
                    self.domains[x].remove(xWord)
                    revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #Establish the initial queue
        if arcs:
            queue = arcs
        else:
            queue = []
            #Loop through every pair of variables
            for var1 in self.crossword.variables:
                for var2 in self.crossword.variables:
                    #If they are not the same variable
                    if var1 != var2:
                        #Add them to the queue
                        queue.append((var1, var2))

        #While there are arcs in the queue
        while queue:
            arc = queue.pop(0)
            x = arc[0]
            y = arc[1]
            if self.revise(x, y): #If x's domain was modified
                if len(self.domains[x]) == 0: 
                     return False #Unsolvable if a variable's domain is empty
                #Add arcs to the queue which need to be checked because of the modification
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        words = []
        for var in assignment:
            word = assignment[var]
            #Check if lengths match
            if var.length != len(word):
                return False
            #Check for duplicate words
            if word in words:
                return False
            else:
                words.append(word)
            #Check for neighbors
            neighbors = self.crossword.neighbors(var)
            if neighbors:
                #Check for consistent overlaps with neighbors
                for neighbor in neighbors:
                    if neighbor in assignment.keys():
                        overlap = self.crossword.overlaps[var, neighbor]
                        if word[overlap[0]] != assignment[neighbor][overlap[1]]:
                            return False
        return True
                
    def ruledOutValues(self, val, var, assignment):
        neighbors = self.crossword.neighbors(var)
        n = 0
        for neighbor in neighbors:
            if neighbor not in assignment.keys():
                overlap = self.crossword.overlaps[var, neighbor]
                for neighborValue in self.domains[neighbor]:
                    if val[overlap[0]] != neighborValue[overlap[1]]:
                        n += 1
        return n

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        sortedDomain = sorted(self.domains[var], key = lambda val: self.ruledOutValues(val, var, assignment))
        return sortedDomain

    def domainLength(self, var):
        """
        Determines the length of a domain for a Variable 'var'
        """
        return len(self.domains[var])

    def numNeighbors(self, var):
        """
        Determines the number of neighbors for a Variable 'var'
        """
        return len(self.crossword.neighbors(var))

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassignedVars = []
        for var in self.crossword.variables:
            if var not in assignment.keys():
                unassignedVars.append(var)
        if not unassignedVars:
            return None
        minRemainingValues = sorted(unassignedVars, key = lambda unassignedVar: self.domainLength(unassignedVar))
        n = 0
        for i in range(len(minRemainingValues)):
            if len(minRemainingValues) <= i+1:
                break
            if(len(self.domains[minRemainingValues[i]]) != len(self.domains[minRemainingValues[i+1]])):
                n = i
                break
        if n > 0:
            mostNeighbors = sorted(minRemainingValues[:n+1:], key = lambda unassignedVar: self.numNeighbors(unassignedVar))
            return mostNeighbors[-1]
        else:
            return minRemainingValues[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            newAssignment = assignment.copy() #Create a copy of the assignment to check if value is consistent
            newAssignment[var] = val #Add the value to the assignment
            if self.consistent(newAssignment): #If value is consistent with assignment
                result = self.backtrack(newAssignment)
                if result is not None:
                    return result
        return None       
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    startTime = time.perf_counter()
    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()
    endTime = time.perf_counter()
    taskTime = endTime-startTime
    # Print result
    if assignment is None:
        print("No solution.")
    else:
        print("Task finished in %.3f seconds" % taskTime)
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
