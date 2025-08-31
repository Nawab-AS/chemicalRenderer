import re as regex
prefixes = ['METH', 'ETH', 'PROP', 'BUT', 'PENT', 'HEX', 'HEPT', 'OCT', 'NON']
prefixes_re = "(" + "|".join(prefixes) + ")"
chain_endings = {"alkane": "ane", "alkene": "ene", "alkyne": "yne"}

# For refrence, all of the organic chemistry in the comments
# will be according to IUPAC nomenclature.

class Substance:
    def __init__(self, name: str):
        self.name = name
        self.formula = self.parse()


    def parse(self):
        #alkyl_branches = fr"(\d,?)+-{prefixes_re}yl" # regex to 
        #((\d,?),?)*-(METH|ETH|PROP|BUT|PENT|HEX|HEPT|OCT|NON)yl
        #alkyl_branches = (regex.findall(simple_alkyl_branches, name))
        """
        step 1: extract (and remove) branches/sub-branches (TODO)
        
        There are two main ways to notate branches

         - Simple substituants
            These are writen as: '(locant),(locant)-[prefix][substituent name]'

         - Complex substituants
            These are writen as: '(locant)-([complex substituent name])[parent name]'

        """

        # step 2: get parent chain
        parent_chain = self.get_parent_chain()

        # step 3: apply the branches onto the parent chain (TODO)

        # step 4: generate image

    def get_parent_chain(self):
        name2 = self.name

        # step 1: get chain type
        self.chain_type = None


        for type, ending in chain_endings.items():
            if name2.endswith(ending):
                self.chain_type = type
                name2 = name2[:len(name2)-len(ending)]
                break

        if self.chain_type == None: 
            raise ValueError("chain type not recognized")


        # step 2: get chain length
        self.chain_length = None

        for i in range(len(prefixes)):
            if name2.upper().endswith(prefixes[i]):
                self.chain_length = i+1
                #name2 = name2[:len(name2)-len(prefixes[i])]
                break

        if self.chain_length == None:
            raise ValueError("chain length not recognized")


        print(self.name, "is an", self.chain_type, "with a parent chain length of", self.chain_length)










