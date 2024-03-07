import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import TextBox
import numpy as np


BUTTON_PRESSED = True


def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def midpoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)


def on_hover(event):
    global BUTTON_PRESSED
    if not BUTTON_PRESSED:
        return
    if event.inaxes == ax1:
        x, y = event.xdata, event.ydata
        draw_triangle(x, y)


def on_click(event):
    global BUTTON_PRESSED
    BUTTON_PRESSED = not BUTTON_PRESSED
    
    if BUTTON_PRESSED:
        ax2.set_facecolor("white")
    else:
        ax2.set_facecolor("thistle")

    if event.inaxes == ax1:
        x, y = event.xdata, event.ydata
        draw_triangle(x, y)

def is_valid(x, y):
    invalid_conditions = [
        x*y < 0.5,
        x < 0.5,
        y < 0.5,
        x > 1,
        y > 1,
    ]
    if any(invalid_conditions):
        return False
    return True


def draw_triangle(x, y):
    if not is_valid(x, y):
        return
    mu = x
    t = y
    mod_k1 = 1

    ax2.clear()
    ax1.set_xlim([mu_min, mu_max])
    ax1.set_ylim([t_min, t_max])
    refresh_ax1()
    ax1.scatter(mu, t, color='blue', s=50, alpha=1)
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1])

    ax2.set_title('$(k_1, k_2, k_3)$ output space')
    # ax2.axis('equal')

    ax2.plot([0, 0.5], [0, np.sqrt(3)/2], 'k--', alpha=0.5, linewidth=1)
    ax2.plot([1, 0.5], [0, np.sqrt(3)/2], 'k--', alpha=0.5, linewidth=1)
    


    points = np.array([
        (0, 0), # left
        (mod_k1, 0), # right
        (t*mu*mod_k1, t*mod_k1*np.sqrt(1-mu**2)) # top
    ])
    triangle = Polygon(
        points,
        closed=True,
        edgecolor='black',
        facecolor='blueviolet',
        alpha=0.5,
        linewidth=1
    )
    ax2.add_patch(triangle)




    # Label sides and angle
    ax2.text(*midpoint(points[0], points[1]), '$k_1$', ha='center', va='bottom', fontsize=12)
    ax2.text(*midpoint(points[0], points[2]), '$k_2$', ha='left', va='top', fontsize=12)
    ax2.text(*midpoint(points[1], points[2]), '$k_3$', ha='right', va='top', fontsize=12)

    prnt_str1 = f"""
$\mu$:  {mu:.06f}
$t$:  {t:.06f}
""".strip("\n")
    prnt_str2 = f"""
$k_1$:  {distance(points[1], points[0]):.06f}
$k_2$:  {distance(points[2], points[0]):.06f}
$k_3$:  {distance(points[2], points[1]):.06f}
""".strip("\n")
    ax2.text(0, 0.95, prnt_str1, ha='left', va='top', fontsize=12, family='monospace')
    ax2.text(1, 0.95, prnt_str2, ha='right', va='top', fontsize=12, family='monospace')


    fig.canvas.draw_idle()


def submit(text):
    try:
        x, y = map(float, text.split(','))
        print(f"Received: {x}, {y}: {'Valid' if is_valid(x, y) else 'Invalid'}")
        global BUTTON_PRESSED
        BUTTON_PRESSED = False
        ax2.set_facecolor("thistle")
        draw_triangle(x, y)
    except ValueError:
        print("Invalid input. Please enter a valid float number.")


# Create the main figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

def refresh_ax1():
    ax1.clear()
    ax1.set_xlim([mu_min, mu_max])
    ax1.set_ylim([t_min, t_max])
    ax1.set_xlabel('$\mu$')
    ax1.set_ylabel('$t$')
    ax1.set_xticks(np.arange(mu_min, mu_max+0.1, 0.1))
    ax1.set_yticks(np.arange(t_min, t_max+0.1, 0.1))
    ax1.set_title('$(\mu, t)$ input space')
    ax1.plot([mu_min, mu_max], [t_min, t_max], 'k--', alpha=0.5, linewidth=1)
    ax1.contourf(MU, T, condition, levels=[-1, 0, 1], colors=['lightcoral', 'palegreen'])
    ax1.axis('equal')

# Create the mu-t plot
## Setup
mu_min = 0.5
mu_max = 1
t_min = 0.5
t_max = 1

mu_vals = np.linspace(mu_min, mu_max, 500)
t_vals  = np.linspace(t_min,  t_max,  500)

ax2.set_xlim([0, 1])
ax2.set_ylim([0, 1])

## Plot titles
ax2.set_title('$(k_1, k_2, k_3)$ output space')

## plotting mu*t >= 0.5 contour
MU, T = np.meshgrid(mu_vals, t_vals)
condition = MU * T > 0.5

## Creating the k1-k2-k3 plot on hover
fig.canvas.mpl_connect('motion_notify_event', on_hover)
fig.canvas.mpl_connect('button_press_event', on_click)


ax2.axis('equal')
refresh_ax1()

# Setting up button for t and mu input
plt.subplots_adjust(bottom=0.3)
text_box_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
text_box = TextBox(text_box_ax, 'Input comma separated $\mu$, t pair:', initial='')
text_box.on_submit(submit)


plt.show()
