# 3D_gas_simulation
- bernoulli.py

This Python code simulates the molecular dynamics of gas particles in a 3D container. It visualizes the movement and collisions of particles, while dynamically calculating kinetic energy and pressure. The simulation allows interactive control of temperature (via particle speed) and container volume using sliders, providing real-time updates on how these changes affect the system's physical properties. The visualization includes both a 3D particle movement plot and 2D graphs for kinetic energy and pressure over time.
---
- bernou_collision.py

The same as bernoulli.py but with collision between molecules.
---
- bernou_final.py

This code simulates the movement of gas molecules inside a 3D box, tracking their velocities and positions over time. It uses the NumPy library to initialize random positions and velocities for 1000 particles, confined within a cube with boundaries between -10 and 10 units. The particles move and collide with the box's walls, changing direction upon impact. The simulation calculates the kinetic energy, pressure, and center of mass over time, and visualizes the particle motion using Matplotlib.

At the end of the simulation, the code generates:

  A 3D plot of particle movement.
  A histogram of the particle velocities.
  A distribution of particles along slices of the X-axis, colored by average velocity.

This allows for visual and quantitative analysis of particle behavior, such as velocity distribution and spatial arrangement.
