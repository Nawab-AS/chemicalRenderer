# Chemical Renderer

![hackatime badge](https://hackatime-badge.hackclub.com/U0857UWECTS/chemicalRenderer)


ChemicalRenderer is a single file python module that can parse standard IUPAC chemical
formulae and turn them into svgs.


## Installation


chemicalRenderer is build from the ground up for its simplistic with a minimalist approach.
Because of this, there are **no external dependencies** simplifying the installation process

1.	Clone the repository with 

```bash
git clone https://github.com/Nawab-AS/chemicalRenderer.git
```

2. Copy the `chemical_renderer.py` file into the same directory as your python project


## Demo


ChemicalRenderer has a simple interactive demo `demo.py`, to run it simply navigate to
the chemicalRenderer source code directory in your terminal and run 

```bash
python3 demo.py
```


## Usage

Import the module with

```python
import chemical_renderer
```

The chemical_renderer.Molecule constructor takes one argument, the name of your organic molecule.
If the name of the molecule is invalid or unrecognized, it will raise a 
`chemical_renderer.ParseError`


### Example
```python
my_molecule = chemical_renderer.Molecule('propene')
```


Once your molecule is parsed, you can render them into SVGs using the `render` method.
You can also get a simple description with the `description` method

### Example
```python
my_molecule = chemical_renderer.Molecule('hex-2,4-ene')

print(my_molecule.description())

# Outputs: hex-2,4-ene is an alkene with a length of 6 and has 2 double bonds between
# 		   the (2 and 3 locants), (4 and 5 locants).

my_molecule.render('my_molecule.svg') # saves an svg of 'hex-2,4-ene' in 'my_molecule.svg'
```

## Screenshot

![hex-2-ene](https://ec52f53a29e871d45d4f0e4c2c3cc187.r2.cloudflarestorage.com/siege-mahadk/ryxm7iyhxfein69zxgp5fjdgmkhr?response-content-disposition=inline%3B%20filename%3D%22Screen%20Shot%202025-10-07%20at%2012.02.48%20AM.png%22%3B%20filename%2A%3DUTF-8%27%27Screen%2520Shot%25202025-10-07%2520at%252012.02.48%2520AM.png&response-content-type=image%2Fpng&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=d7cf99256938357bf3eaa33a12e24908%2F20251007%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20251007T040558Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=79b09bb876ea32df113bd9f69fe5800b3fe6de1382615de5587b33ed8592e35a)


## Contributing


Pull requests are welcome, especially due to the fact that I don't have a complete understanding of organic chemistry nomenclature,
but for major changes, please open an issue to discuss what you would like to change/add.



## Roadmap


There is a lot of room for improvement to this project, future improvements include but
are not limited to:

 -	parsing branches (and sub-branchs)

 -	support for other chain types (alcohols, aldehydes, ketones, carboxylic acids, and amines)

 -	turning this into an API (and monetize)?

