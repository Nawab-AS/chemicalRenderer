import re as regex
prefixes = ['METH', 'ETH', 'PROP', 'BUT', 'PENT', 'HEX', 'HEPT', 'OCT', 'NON']
#prefixes_re = "(" + "|".join(prefixes) + ")"
chain_endings = {"alkane": "ane", "alkene": "ene", "alkyne": "yne"}

class ParseError(Exception): # custom error class
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# For refrence, all of the organic chemistry in the comments
# will be according to IUPAC nomenclature.

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

    
    @staticmethod
    def _get_chain_length(name: str):
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


    @staticmethod
    def _get_bond_pos(name: str):
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


    # rendering methods (TODO, for now it will return a description) 


    def description(self):
        try: 
            return (getattr(self, "_describe_"+self.chain_type)())
        except AttributeError as err:
            print("\033[1m\033[33m","Error: Organic_Chemical class doesn't contain a",
                        "_describe_"+self.chain_type, "function", "\033[0m")


    def _describe_alkane(self):
        return f"{self.name} is an alkane with a length of {self.chain_length}."


    def _describe_alkene(self):
        double_bond = []
        for pos in self.double_bond_locant:
            double_bond.append(f"({pos} and {pos + 1} locants)")

        return f"{self.name} is an alkene with a length of {self.chain_length} " \
            + f"and has {len(double_bond)} double bond{"" if len(double_bond)==0 else "s"} " \
            + f"between the {", ".join(double_bond)}."


    def _describe_alkyne(self):
        triple_bond = []
        for pos in self.triple_bond_locant:
            triple_bond.append(f"({pos} and {pos + 1} locants)")

        return f"{self.name} is an alkyne with a length of {self.chain_length} " \
            + f"and has {len(triple_bond)} triple bond{"" if len(triple_bond)==0 else "s"} " \
            + f"between the {", ".join(triple_bond)}."
