class renderer:
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

    def render(self):
        carbons = []
        bonds = []


        for xPos, conn in self.carbons.items():
            print(f"Rendering carbon at {xPos} with connections {conn}")
            # draw carbon
            carbons.append(self._get_carbon((xPos, 0), conn))

            # draw bonds
            if conn[0] != 0:
                bonds.append(str(xPos)+", left")
                bonds.append(self._get_horizontal_bond(conn[0], (xPos-1, 0)))
            if conn[1] != 0:
                bonds.append(str(xPos)+", right")
                bonds.append(self._get_horizontal_bond(conn[1], (xPos, 0)))

        # make the lists unique
        carbons = list(dict.fromkeys(carbons))
        bonds = list(dict.fromkeys(bonds))

        size = (len(carbons) * 80 - 35, 30)

        return ( f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}">\n'
                + "<style>text{text-anchor:middle;width:45px;dominant-baseline:middle;font-size:24px;}path{stroke:black;stroke-width:2;transform:translate(0px,-2px);}</style>\n" 
                + '<g transform="translate(23, 15)">\n\n'
                + '<g transform="translate(25, 0)">' + "\n".join(bonds) + "\n" + "</g>\n\n"
                + "\n".join(carbons) 
                + "\n\n</g>\n</svg>"
               )

if __name__ == "__main__":
    r = renderer()
    r.add_carbon(1, (1, 0))
    r.add_carbon(2, (3, 0))
    r.add_carbon(3, (1, 0))
    r.add_carbon(4, (1, 0))
    with open("test2.svg", "w") as f:
        f.write(r.render())