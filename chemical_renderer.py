""" ==========================================================
File:        chemical_renderer.py
Description: A python module that can convert standard IUPAC
               chemical formulae and turn them into svgs.
Maintainer:  nawab-as <support@nawab-as.software>
License:     MIT, see LICENSE for more details.
==========================================================="""

# For refrence, all of the organic chemistry in the comments
# will be according to IUPAC nomenclature.

import re as regex
prefixes = ['METH', 'ETH', 'PROP', 'BUT', 'PENT', 'HEX', 'HEPT', 'OCT', 'NON']
#prefixes_re = "(" + "|".join(prefixes) + ")"
chain_endings = {"alkane": "ane", "alkene": "ene", "alkyne": "yne"}

class ParseError(Exception): # custom error class
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

def quantify(n: int):
    if n == 1: return '1st'
    if n == 2: return '2nd'
    if n == 3: return '3rd'
    return str(n) + 'th'

class Molecule:
    def __init__(self, name: str):
        self.name = name
        self.formula = self._parse()


    # parsing functions


    def _parse(self):
        # step 1: get parent chain
        parent_chain = self._parent_chain()

        #alkyl_branches = fr"(\d,?)+-{prefixes_re}yl" # regex to 
        #((\d,?),?)*-(METH|ETH|PROP|BUT|PENT|HEX|HEPT|OCT|NON)yl
        #alkyl_branches = (regex.findall(simple_alkyl_branches, name))
        """
        step 2: get all branches/sub-branches (TODO)
        
        There are two main ways to notate branches

         - Simple substituants
            These are writen as: '(locant),(locant)-[prefix][substituent name]'

         - Complex substituants
            These are writen as: '(locant)-([complex substituent name])[parent name]'

        """

        # step 3: apply the branches onto the parent chain (TODO)

        # step 4: generate image


    def _parent_chain(self):
        """
        This function takes self.name and determines the chain type. Using this,
        it dynamically calls '_parse_<chain type>' (replace '<chain type>' with
        the actual chain type)
        """
        self.chain_type = None
        
        for type, ending in chain_endings.items():
            if self.name.endswith(ending):
                self.chain_type = type
                try: 
                    return (getattr(self, "_parse_"+type)())
                except AttributeError as err:
                    print("\033[1m\033[33m","Error: Organic_Chemical class doesn't contain a",
                        "_parse_"+type, "function", "\033[0m")
                break

        if self.chain_type == None: 
            raise ParseError("chain type not recognized")

    
    def _get_chain_length(self, name: str):
        """
        This function takes the name of the chemical with the ending (chain type)
        removed and returns a tuple of the chain length followed by the new string
        with the chain length prefix removed.
        """
        for i in range(len(prefixes)):
            if name.lower().endswith(prefixes[i].lower()):
                chain_length = i + 1
                new_name = name[:-len(prefixes[i])]
                return (chain_length, new_name)

        # if no matching prefix is found, throw an error
        raise ParseError("chain length not recognized")


    def _get_bond_pos(self, name: str):
        """
        This function matches the end of the name and finds all of the locants.
        It returns a regex.matchObject, or if the bond locants were not found, it
        returns None.
        """

        return regex.search(r"-(\d+,?)+-$", name)


    def _parse_alkane(self):
        self.chain_length = None
        name2 = self.name[:-3] # remove '-ane' suffix

        self.chain_length, name2 = self._get_chain_length(name2)


    def _parse_alkene(self):
        self.chain_length = None
        name2 = self.name[:len(self.name)-3] # remove '-ene' suffix

        # get position of double bond
        self.double_bond_locant = None
        bond_pos = self._get_bond_pos(name2)
        if bond_pos:
            name2 = name2[:-len(bond_pos.group())] # remove bond position from the end

            # this will not give an error if the regex is matched
            bond_pos = [int(pos) for pos in bond_pos.group()[1:-1].split(',')]

        self.chain_length, name2 = self._get_chain_length(name2)

        if not bond_pos:
            if self.chain_length <= 3:
                bond_pos = [1]
            else:
                raise ParseError("alkenes with a chain length of 4 or more need a double bond locant")

        if len(bond_pos) != len(set(bond_pos)):
            raise ParseError("duplicate double bond positions are not allowed")

        if self.chain_length < 2:
            raise ParseError("alkenes need a minumum chain length of two")

        for pos in bond_pos:
            if pos >= self.chain_length or pos < 1:
                raise ParseError("double bond position is out or range")

        self.double_bond_locant = bond_pos


    def _parse_alkyne(self):
            self.chain_length = None
            name2 = self.name[:len(self.name)-3] # remove '-yne' suffix

            # get position of double bond
            self.triple_bond_locant = None
            bond_pos = self._get_bond_pos(name2)
            if bond_pos:
                name2 = name2[:-len(bond_pos.group())] # remove bond position from the end

                # this will not give an error if the regex is matched
                bond_pos = [int(pos) for pos in bond_pos.group()[1:-1].split(',')]

            self.chain_length, name2 = self._get_chain_length(name2)

            if not bond_pos:
                if self.chain_length <= 3:
                    bond_pos = [1]
                else:
                    raise ParseError("alkynes with a chain length of 4 or more need a triple bond locant")

            if len(bond_pos) != len(set(bond_pos)):
                raise ParseError("duplicate triple bond positions are not allowed")

            if self.chain_length < 2:
                raise ParseError("alkynes need a minumum chain length of two")

            for pos in bond_pos:
                if pos >= self.chain_length or pos < 1:
                    raise ParseError("triple bond position is out or range")

            self.triple_bond_locant = bond_pos


    # description methods

    def description(self):
        try: 
            return (getattr(self, "_describe_"+self.chain_type)())
        except AttributeError as err:
            print("\033[1m\033[33m","Error: Organic_Chemical class doesn't contain a",
                        "_describe_"+self.chain_type, "function", "\033[0m")


    def _describe_alkane(self):
        return f"{self.name} is an alkane with a length of {self.chain_length}."


    def _describe_alkene(self):
        if self.double_bond_locant is None:
            raise ValueError("double bond locants not recognized, cannot describe molecule")

        double_bond = []
        for pos in self.double_bond_locant:
            double_bond.append(f"({pos} and {pos + 1} locants)")

        return f"{self.name} is an alkene with a length of {self.chain_length} " \
            + f"and has {len(double_bond)} double bond(s) " \
            + f"between the {', '.join(double_bond)}."


    def _describe_alkyne(self):
        if self.triple_bond_locant is None:
            raise ValueError("triple bond locants not recognized, cannot describe molecule")

        triple_bond = []
        for pos in self.triple_bond_locant:
            triple_bond.append(f"({pos} and {pos + 1} locants)")

        return f"{self.name} is an alkyne with a length of {self.chain_length} " \
            + f"and has {len(triple_bond)} triple bond{'' if len(triple_bond)==0 else 's'} " \
            + f"between the {', '.join(triple_bond)}."


    # rendering methods

    def render(self, file_name: str = ''):
        try: 
            if file_name == '':
                return (getattr(self, "_render_"+self.chain_type)())


            with open(file_name, 'w') as f:
                f.write(getattr(self, "_render_"+self.chain_type)())
            
        except AttributeError as err:
            print("\033[1m\033[33m","Error: Organic_Chemical class doesn't contain a",
                        "_render_"+self.chain_type, "function", "\033[0m")
    
    def _render_alkane(self):
        r = Renderer()
        for i in range(1, self.chain_length): # type: ignore
            r.add_carbon(i, (1, 0))
        return r.render()


    def _render_alkene(self):
        r = Renderer()
        for i in range(1, self.chain_length): # type: ignore
            if i in self.double_bond_locant:
                r.add_carbon(i, (2, 0))
            else:
                r.add_carbon(i, (1, 0))
        return r.render()


    def _render_alkyne(self):
        r = Renderer()
        for i in range(1, self.chain_length): # type: ignore
            if i in self.triple_bond_locant:
                r.add_carbon(i, (3, 0))
            else:
                r.add_carbon(i, (1, 0))
        return r.render()


class Renderer:
    def __init__(self):
        """ Initializes with a single carbon at position 0 """
        self.carbons = {}
        self.add_carbon(0, (0, 0))

    def add_carbon(self, xPos: int, conn: tuple[int, int]):
        """
        conn[0] is for right connections
        conn[1] is for left connections

        conn = 1  =>  single bond
        conn = 2  =>  double bond
        conn = 3  =>  triple bond
        """
        if conn[0] < 0 or conn[0] > 3 or conn[1] < 0 or conn[1] > 3:
            raise ValueError("connection values must be between 0 and 3")

        if xPos in self.carbons:
            raise ValueError(f"Carbon already exists at position {xPos}")
        
        self.carbons[xPos] = conn

        # check and update nearby carbons
        for xDir in [0, 1]:
            if conn[xDir] == 0: continue # no bond, skip

            if self.carbons.get(xPos + (xDir*2-1), None) is not None: # neighbouring carbon exists
                if xDir == 0: # left connection
                    self.carbons[xPos - 1] = ( self.carbons[xPos - 1][0], conn[0] )
                else: # right connection
                    self.carbons[xPos + 1] = ( conn[1], self.carbons[xPos + 1][1] )

    # overload for tuple input => delegate to other method
    def _get_absolute_pos(self, pos: tuple[int, int]) -> tuple[int, int]: 
        return (pos[0] * 80, pos[1] * 80) # scale

    def _get_horizontal_bond(self, num_bonds: int, pos: tuple[int, int]) -> str:
        BOND_LENGTH = 30

        pos = self._get_absolute_pos(pos) # scale
        
        if num_bonds == 1: # single bond
            return f'<path d="M {pos[0]} {pos[1]} h {BOND_LENGTH}"/>'

        elif num_bonds == 2: # double bond
            return ( \
                f'<path d="M {pos[0]} {pos[1]-3} h {BOND_LENGTH}"/>\n' + \
                f'<path d="M {pos[0]} {pos[1]+3} h {BOND_LENGTH}"/>' \
            )

        elif num_bonds == 3: # triple bond
            return ( \
                f'<path d="M {pos[0]} {pos[1]-5} h {BOND_LENGTH}"/>\n' + \
                f'<path d="M {pos[0]} {pos[1]} h {BOND_LENGTH}"/>\n' + \
                f'<path d="M {pos[0]} {pos[1]+5} h {BOND_LENGTH}"/>' \
            )
        else:
            raise ValueError("num_bonds must be 1, 2, or 3")
    
    def _get_carbon(self, pos: tuple[int, int], conn: tuple[int, int] = (0,0)) -> str:
        pos = self._get_absolute_pos(pos) # scale

        if (abs(conn[0]) + abs(conn[1])) > 4:
            raise ValueError("Too many connections to carbon")
        
        if conn[0] < 0 or conn[0] > 3 or conn[1] < 0 or conn[1] > 3:
            raise ValueError("connection values must be between 0 and 3")

        hydrogens = 4 - (conn[0] + conn[1])
        text = ["C", "CH", "CH₂", "CH₃", "CH₄"][hydrogens]

        return f'<text x="{pos[0]}" y="{pos[1]}">{text}</text>'

    def render(self, file_name: str = ''):
        carbons = []
        bonds = []

        for xPos, conn in self.carbons.items():
            #print(f"Rendering carbon at {xPos} with connections {conn}")
            # draw carbon
            carbons.append(self._get_carbon((xPos, 0), conn))

            # draw bonds
            if conn[0] != 0:
                # bonds.append(str(xPos)+", left")
                bonds.append(self._get_horizontal_bond(conn[0], (xPos-1, 0)))
            if conn[1] != 0:
                # bonds.append(str(xPos)+", right")
                bonds.append(self._get_horizontal_bond(conn[1], (xPos, 0)))

        # make the lists unique
        carbons = list(dict.fromkeys(carbons))
        bonds = list(dict.fromkeys(bonds))

        size = (len(carbons) * 80 - 35, 30)

        svg =  ( f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}">\n'
                + "<style>text{text-anchor:middle;width:45px;dominant-baseline:middle;font-size:24px;}path{stroke:black;stroke-width:2;transform:translate(0px,-2px);}</style>\n" 
                + '<g transform="translate(23, 15)">\n\n'
                + '<g transform="translate(25, 0)">' + "\n".join(bonds) + "\n" + "</g>\n\n"
                + "\n".join(carbons) 
                + "\n\n</g>\n</svg>"
               )
        
        if file_name == '': return svg

        with open(file_name, "w") as f:
            f.write(svg)