"""
Hannibal Barca Optimizer (HBO) - Python Translation
Original Authors: Ghaith Manita, Mohamed Wajdi Ouertani, Ouajdi Korbaa
Python Translation by Assistant

Main paper: M.W. Ouertani, G. Manita, O. Korbaa
Hannibal Barca optimizer: the power of the pincer movement for global optimization 
and multilevel image thresholding, Cluster Computing
DOI: 10.1007/s10586-025-05134-1
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from benchmark_functions import get_functions_details
from hbo_optimizer import HBO

def main():
    """Main execution function"""
    # Clear console equivalent
    print("=" * 60)
    print("Hannibal Barca Optimizer (HBO) - Python Implementation")
    print("=" * 60)

    # Parameters
    warriors_no = 30  # Number of search agents
    function_name = 'F3'  # Name of test function (F1 to F23)
    max_iteration = 1000  # Maximum number of iterations

    # Load details of the selected benchmark function
    lb, ub, dim, fobj = get_functions_details(function_name)

    # Run HBO optimization
    print(f"\nRunning HBO on {function_name} with {warriors_no} warriors for {max_iteration} iterations...")
    print(f"Problem dimension: {dim}")
    print(f"Search bounds: [{lb}, {ub}]")
    print("-" * 60)

    best_score, best_pos, hbo_curve = HBO(warriors_no, max_iteration, lb, ub, dim, fobj)

    # Display results
    print(f"\nOptimization completed!")
    print(f"Best solution found: {best_pos}")
    print(f"Best fitness value: {best_score:.6e}")

    # Create visualization
    create_plots(function_name, fobj, lb, ub, dim, hbo_curve)

def create_plots(function_name, fobj, lb, ub, dim, hbo_curve):
    """Create visualization plots"""
    fig = plt.figure(figsize=(15, 6))

    # Plot parameter space (for 2D functions)
    if dim == 2:
        ax1 = fig.add_subplot(131, projection='3d')
        plot_function_surface(ax1, function_name, fobj, lb, ub)
        ax1.set_title('Parameter Space (3D)')
        ax1.set_xlabel('x₁')
        ax1.set_ylabel('x₂')
        ax1.set_zlabel(f'{function_name}(x₁, x₂)')

        # 2D contour plot
        ax2 = fig.add_subplot(132)
        plot_function_contour(ax2, function_name, fobj, lb, ub)
        ax2.set_title('Parameter Space (Contour)')
        ax2.set_xlabel('x₁')
        ax2.set_ylabel('x₂')
    else:
        ax1 = fig.add_subplot(121)
        ax1.text(0.5, 0.5, f'{function_name}\nDimension: {dim}\nVisualization not available\nfor high-dimensional functions', 
                ha='center', va='center', transform=ax1.transAxes, fontsize=12)
        ax1.set_title('Parameter Space')
        ax1.axis('off')

    # Plot convergence curve
    if dim == 2:
        ax3 = fig.add_subplot(133)
    else:
        ax3 = fig.add_subplot(122)

    ax3.semilogy(hbo_curve, 'r-', linewidth=2, label='HBO')
    ax3.set_title('Convergence Curve')
    ax3.set_xlabel('Iteration')
    ax3.set_ylabel('Best Fitness Value')
    ax3.grid(True, alpha=0.3)
    ax3.legend()

    plt.tight_layout()
    plt.show()

def plot_function_surface(ax, func_name, fobj, lb, ub):
    """Plot 3D surface of benchmark function"""
    if isinstance(lb, (int, float)):
        x_range = np.linspace(lb, ub, 50)
        y_range = np.linspace(lb, ub, 50)
    else:
        x_range = np.linspace(lb[0], ub[0], 50)
        y_range = np.linspace(lb[1] if len(lb) > 1 else lb[0], 
                             ub[1] if len(ub) > 1 else ub[0], 50)

    X, Y = np.meshgrid(x_range, y_range)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = fobj([X[i, j], Y[i, j]])

    # Handle extreme values for better visualization
    Z = np.clip(Z, np.percentile(Z, 1), np.percentile(Z, 99))

    surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.8, 
                          linewidth=0, antialiased=True)
    ax.view_init(elev=20, azim=45)

def plot_function_contour(ax, func_name, fobj, lb, ub):
    """Plot 2D contour of benchmark function"""
    if isinstance(lb, (int, float)):
        x_range = np.linspace(lb, ub, 100)
        y_range = np.linspace(lb, ub, 100)
    else:
        x_range = np.linspace(lb[0], ub[0], 100)
        y_range = np.linspace(lb[1] if len(lb) > 1 else lb[0], 
                             ub[1] if len(ub) > 1 else ub[0], 100)

    X, Y = np.meshgrid(x_range, y_range)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = fobj([X[i, j], Y[i, j]])

    # Handle extreme values for better visualization
    Z = np.clip(Z, np.percentile(Z, 1), np.percentile(Z, 99))

    contour = ax.contour(X, Y, Z, levels=20, cmap=cm.viridis)
    ax.contourf(X, Y, Z, levels=20, cmap=cm.viridis, alpha=0.6)
    plt.colorbar(contour, ax=ax, shrink=0.8)

if __name__ == "__main__":
    main()
