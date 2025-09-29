import numpy as np

def get_functions_details(F):
    """Get details of benchmark functions F1-F23"""
    functions = {
        'F1': {'fobj': F1, 'lb': -100, 'ub': 100, 'dim': 30},
        'F2': {'fobj': F2, 'lb': -10, 'ub': 10, 'dim': 30},
        'F3': {'fobj': F3, 'lb': -100, 'ub': 100, 'dim': 30},
        'F4': {'fobj': F4, 'lb': -100, 'ub': 100, 'dim': 30},
        'F5': {'fobj': F5, 'lb': -30, 'ub': 30, 'dim': 30},
        'F6': {'fobj': F6, 'lb': -100, 'ub': 100, 'dim': 30},
        'F7': {'fobj': F7, 'lb': -1.28, 'ub': 1.28, 'dim': 30},
        'F8': {'fobj': F8, 'lb': -500, 'ub': 500, 'dim': 30},
        'F9': {'fobj': F9, 'lb': -5.12, 'ub': 5.12, 'dim': 30},
        'F10': {'fobj': F10, 'lb': -32, 'ub': 32, 'dim': 30},
        'F11': {'fobj': F11, 'lb': -600, 'ub': 600, 'dim': 30},
        'F12': {'fobj': F12, 'lb': -50, 'ub': 50, 'dim': 30},
        'F13': {'fobj': F13, 'lb': -50, 'ub': 50, 'dim': 30},
        'F14': {'fobj': F14, 'lb': -65.536, 'ub': 65.536, 'dim': 2},
        'F15': {'fobj': F15, 'lb': -5, 'ub': 5, 'dim': 4},
        'F16': {'fobj': F16, 'lb': -5, 'ub': 5, 'dim': 2},
        'F17': {'fobj': F17, 'lb': [-5, 0], 'ub': [10, 15], 'dim': 2},
        'F18': {'fobj': F18, 'lb': -2, 'ub': 2, 'dim': 2},
        'F19': {'fobj': F19, 'lb': 0, 'ub': 1, 'dim': 3},
        'F20': {'fobj': F20, 'lb': 0, 'ub': 1, 'dim': 6},
        'F21': {'fobj': F21, 'lb': 0, 'ub': 10, 'dim': 4},
        'F22': {'fobj': F22, 'lb': 0, 'ub': 10, 'dim': 4},
        'F23': {'fobj': F23, 'lb': 0, 'ub': 10, 'dim': 4}
    }
    
    details = functions[F]
    return details['lb'], details['ub'], details['dim'], details['fobj']

# Benchmark function implementations (F1-F23)
def F1(x):
    return np.sum(x**2)

def F2(x):
    return np.sum(np.abs(x)) + np.prod(np.abs(x))

def F3(x):
    dim = len(x)
    o = 0
    for i in range(dim):
        o += np.sum(x[:i+1])**2
    return o

def F4(x):
    return np.max(np.abs(x))

def F5(x):
    dim = len(x)
    return np.sum(100*(x[1:dim] - x[0:dim-1]**2)**2 + (x[0:dim-1] - 1)**2)

def F6(x):
    return np.sum(np.abs(x + 0.5)**2)

def F7(x):
    dim = len(x)
    return np.sum(np.arange(1, dim+1) * (x**4)) + np.random.rand()

def F8(x):
    return np.sum(-x * np.sin(np.sqrt(np.abs(x))))

def F9(x):
    dim = len(x)
    return np.sum(x**2 - 10*np.cos(2*np.pi*x)) + 10*dim

def F10(x):
    dim = len(x)
    return -20*np.exp(-0.2*np.sqrt(np.sum(x**2)/dim)) - np.exp(np.sum(np.cos(2*np.pi*x))/dim) + 20 + np.e

def F11(x):
    dim = len(x)
    return np.sum(x**2)/4000 - np.prod(np.cos(x/np.sqrt(np.arange(1, dim+1)))) + 1

def F12(x):
    dim = len(x)
    term1 = 10 * (np.sin(np.pi * (1 + (x[0] + 1)/4)))**2
    term2 = np.sum(((x[:-1] + 1)/4)**2 * (1 + 10 * (np.sin(np.pi * (1 + (x[1:] + 1)/4)))**2))
    term3 = ((x[-1] + 1)/4)**2
    penalty = np.sum(Ufun(x, 10, 100, 4))
    return (np.pi/dim) * (term1 + term2 + term3) + penalty

def F13(x):
    dim = len(x)
    term1 = (np.sin(3*np.pi*x[0]))**2
    term2 = np.sum((x[:-1] - 1)**2 * (1 + (np.sin(3*np.pi*x[1:]))**2))
    term3 = ((x[-1] - 1)**2) * (1 + (np.sin(2*np.pi*x[-1]))**2)
    penalty = np.sum(Ufun(x, 5, 100, 4))
    return 0.1 * (term1 + term2 + term3) + penalty

def F14(x):
    aS = np.array([[-32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32],
                   [-32, -32, -32, -32, -32, -16, -16, -16, -16, -16, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 32, 32, 32, 32, 32]])
    bS = np.zeros(25)
    for j in range(25):
        bS[j] = np.sum((x - aS[:, j])**6)
    return (1/500 + np.sum(1/(np.arange(1, 26) + bS)))**(-1)

def F15(x):
    aK = np.array([0.1957, 0.1947, 0.1735, 0.16, 0.0844, 0.0627, 0.0456, 0.0342, 0.0323, 0.0235, 0.0246])
    bK = 1 / np.array([0.25, 0.5, 1, 2, 4, 6, 8, 10, 12, 14, 16])
    return np.sum((aK - (x[0] * (bK**2 + x[1]*bK)) / (bK**2 + x[2]*bK + x[3]))**2)

def F16(x):
    return 4*(x[0]**2) - 2.1*(x[0]**4) + (x[0]**6)/3 + x[0]*x[1] - 4*(x[1]**2) + 4*(x[1]**4)

def F17(x):
    return (x[1] - (x[0]**2)*5.1/(4*(np.pi**2)) + 5/np.pi*x[0] - 6)**2 + 10*(1 - 1/(8*np.pi))*np.cos(x[0]) + 10

def F18(x):
    term1 = 1 + (x[0] + x[1] + 1)**2 * (19 - 14*x[0] + 3*(x[0]**2) - 14*x[1] + 6*x[0]*x[1] + 3*x[1]**2)
    term2 = 30 + (2*x[0] - 3*x[1])**2 * (18 - 32*x[0] + 12*(x[0]**2) + 48*x[1] - 36*x[0]*x[1] + 27*(x[1]**2))
    return term1 * term2

def F19(x):
    aH = np.array([[3, 10, 30], [0.1, 10, 35], [3, 10, 30], [0.1, 10, 35]])
    cH = np.array([1, 1.2, 3, 3.2])
    pH = np.array([[0.3689, 0.117, 0.2673], [0.4699, 0.4387, 0.747], 
                   [0.1091, 0.8732, 0.5547], [0.03815, 0.5743, 0.8828]])
    o = 0
    for i in range(4):
        o -= cH[i] * np.exp(-np.sum(aH[i, :] * ((x - pH[i, :])**2)))
    return o

def F20(x):
    aH = np.array([[10, 3, 17, 3.5, 1.7, 8], [0.05, 10, 17, 0.1, 8, 14],
                   [3, 3.5, 1.7, 10, 17, 8], [17, 8, 0.05, 10, 0.1, 14]])
    cH = np.array([1, 1.2, 3, 3.2])
    pH = np.array([[0.1312, 0.1696, 0.5569, 0.0124, 0.8283, 0.5886],
                   [0.2329, 0.4135, 0.8307, 0.3736, 0.1004, 0.9991],
                   [0.2348, 0.1415, 0.3522, 0.2883, 0.3047, 0.6650],
                   [0.4047, 0.8828, 0.8732, 0.5743, 0.1091, 0.0381]])
    o = 0
    for i in range(4):
        o -= cH[i] * np.exp(-np.sum(aH[i, :] * ((x - pH[i, :])**2)))
    return o

def F21(x):
    return shekel_function(x, 5)

def F22(x):
    return shekel_function(x, 7)

def F23(x):
    return shekel_function(x, 10)

def shekel_function(x, m):
    aSH = np.array([[4, 4, 4, 4], [1, 1, 1, 1], [8, 8, 8, 8], [6, 6, 6, 6], [3, 7, 3, 7],
                    [2, 9, 2, 9], [5, 5, 3, 3], [8, 1, 8, 1], [6, 2, 6, 2], [7, 3.6, 7, 3.6]])
    cSH = np.array([0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.3, 0.7, 0.5, 0.5])
    o = 0
    for i in range(m):
        o -= 1 / (np.sum((x - aSH[i, :])**2) + cSH[i])
    return o

def Ufun(x, a, k, m):
    return k * ((x - a)**m) * (x > a) + k * ((-x - a)**m) * (x < -a)
