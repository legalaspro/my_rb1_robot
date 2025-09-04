import math

def calculate_inertia(shape, mass, dimensions):
    """
    Calculate the principal moments of inertia for basic shapes.
    
    Parameters:
    - shape: str, one of 'cylinder', 'sphere', 'box' (assuming square means cube)
    - mass: float, mass of the object in kg
    - dimensions: dict, shape-specific dimensions
      - For 'cylinder': {'radius': float, 'height': float}
      - For 'sphere': {'radius': float}
      - For 'box': {'x': float, 'y':float,  'z':float}
    
    Returns: tuple of (Ixx, Iyy, Izz) or similar, assuming axis-aligned
    """
    if shape.lower() == 'cylinder':
        r = dimensions.get('radius', 0)
        h = dimensions.get('height', 0)
        # Inertia for cylinder about central axes
        Ixx = (1/12) * mass * (3 * r**2 + h**2)  # Along height
        Iyy = Ixx  # Symmetric
        Izz = (1/2) * mass * r**2  # Perpendicular to height
        return (Ixx, Iyy, Izz)
    
    elif shape.lower() == 'sphere':
        r = dimensions.get('radius', 0)
        # Inertia for sphere (all axes equal)
        I = (2/5) * mass * r**2
        return (I, I, I)
    
    elif shape.lower() == 'box':  
        x = dimensions.get('x', 0)
        y = dimensions.get('y', 0)
        z = dimensions.get('z', 0)
        # Inertia for cube about center axes
        Ixx = (1/12) * mass * (y**2 + z**2) 
        Iyy = (1/12) * mass * (x**2 + z**2) 
        Izz = (1/12) * mass * (y**2 + x**2) 
        return (Ixx, Iyy, Izz)
    
    else:
        raise ValueError("Unsupported shape. Choose 'cylinder', 'sphere', or 'box'.")

def main():
    print("Select shape: 1. Cylinder, 2. Sphere, 3. Box")
    choice = int(input("Enter number: "))
    mass = float(input("Enter mass (kg): "))
    
    if choice == 1:
        shape = 'cylinder'
        r = float(input("Enter radius (m): "))
        h = float(input("Enter height (m): "))
        dims = {'radius': r, 'height': h}
    elif choice == 2:
        shape = 'sphere'
        r = float(input("Enter radius (m): "))
        dims = {'radius': r}
    elif choice == 3:
        shape = 'box'
        x = float(input("Enter side length (x): "))
        y = float(input("Enter side length (y): "))
        z = float(input("Enter side length (z): "))
        dims = {'x': x, 'y':y, 'z':z}
    else:
        print("Invalid choice.")
        return
    
    inertia = calculate_inertia(shape, mass, dims)
    print(f"Inertia for {shape} (Ixx, Iyy, Izz): {inertia}")

if __name__ == "__main__":
    main()