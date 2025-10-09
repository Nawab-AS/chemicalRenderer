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

![hex-2-ene](https://camo.githubusercontent.com/e9869f751dd212abdd401492f732260907653e1faccc900ae92850eb86afa1b5/68747470733a2f2f65633532663533613239653837316434356434663065346332633363633138372e72322e636c6f7564666c61726573746f726167652e636f6d2f73696567652d6d616861646b2f7279786d37697968786665696e36397a78677035666a64676d6b68723f726573706f6e73652d636f6e74656e742d646973706f736974696f6e3d696e6c696e6525334225323066696c656e616d6525334425323253637265656e25323053686f74253230323032352d31302d3037253230617425323031322e30322e3438253230414d2e706e6725323225334225323066696c656e616d652532412533445554462d3825323725323753637265656e253235323053686f742532353230323032352d31302d303725323532306174253235323031322e30322e34382532353230414d2e706e6726726573706f6e73652d636f6e74656e742d747970653d696d616765253246706e6726582d416d7a2d416c676f726974686d3d415753342d484d41432d53484132353626582d416d7a2d43726564656e7469616c3d643763663939323536393338333537626633656161333361313265323439303825324632303235313030372532466175746f2532467333253246617773345f7265717565737426582d416d7a2d446174653d3230323531303037543034303535385a26582d416d7a2d457870697265733d33303026582d416d7a2d5369676e6564486561646572733d686f737426582d416d7a2d5369676e61747572653d37396230396262383736656133326466313133626439663639666535383030623366653664653133383236313564653535383762333365643835393265333561)


## Contributing


Pull requests are welcome, especially due to the fact that I don't have a complete understanding of organic chemistry nomenclature,
but for major changes, please open an issue to discuss what you would like to change/add.



## Roadmap


There is a lot of room for improvement to this project, future improvements include but
are not limited to:

 -	parsing branches (and sub-branchs)

 -	support for other chain types (alcohols, aldehydes, ketones, carboxylic acids, and amines)

 -	turning this into an API (and monetize)?

