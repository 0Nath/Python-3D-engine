# Python-3D-engine
A python simple 3D object rendering made "from stratch"

## Usage

### 3D Engine
The program can be controlled using the mouse and the ZQSD, SPACE, and SHIFT keys.  
A console is available in the terminal. For now, the only supported command is
```
tp x y z
```
where x y and z are ints.


The Simulation class takes several arguments:

- dimensions: a tuple of integers  
- meshs: the meshes to load (see below for more)  
- launcher (optional): a class used if you want to integrate the launcher into another Pygame project.  

The Simulation will call the following attributes:
```
Launcher.screen
Launcher.dimensions
Launcher.font
Launcher.font_color
```
Meaning your Pygame project must have:
- self.screen: the Pygame surface  
- self.dimensions: a tuple of two integers  
- self.font: a Pygame font (pygame.font.Font(...))  
- self.font_color: a tuple of three integers (RGB)  

---

### Additional Classes

Included Mesh class:  
Takes a list of points (see examples below) and a color.

Included Rotating_Mesh class:  
Takes a list of points (see examples below), a color, and three rotation values (x, y, z).

STL Loader classes:  
Includes a Mesh_from_stl class that takes a file path and a color.

---

### Examples of Use
```
meshs = [stl_loader.Mesh_from_stl("name.stl",(255,255,255))
		 ]
Simulation((1920,1080),meshs)

```
![The triple T](images/example2.jpg)
A loaded model.


Use simples shapes:
```
  meshs = [
  Rotating_Mesh([[[-1, -1, -1],[1, -1, -1],[1, 1, -1], [-1, 1, -1],[-1, -1, 1],[1, -1, 1], [1, 1, 1], [-1, 1, 1] ],
  [    [0, 1, 2, 3],  [4, 5, 6, 7],[0, 1, 5, 4],[3, 2, 6, 7],[0, 3, 7, 4],[1, 2, 6, 5]]],(255,0,0),0,0,0.02),

  Mesh([[[1, -1, -1],[3, -1, -1],[3, 1, -1], [1, 1, -1],[1, -1, 1],[3, -1, 1], [3, 1, 1], [1, 1, 1] ],
  [    [0, 1, 2, 3],  [4, 5, 6, 7],[0, 1, 5, 4],[3, 2, 6, 7],[0, 3, 7, 4],[1, 2, 6, 5]]],(0,0,255))
  ]
  	Simulation((1920,1080),meshs)

```
![Simple shapes](images/example1.jpg)
