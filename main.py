import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import TextBox, Button
import numpy as np


BUTTON_PRESSED = True
K_LIST = []
SHOW_EQUILATERAL_TRIANGLE = False


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
    refresh_ax1()
    ax1.set_xlim([mu_min, mu_max])
    ax1.set_ylim([t_min, t_max])
    ax1.scatter(mu, t, color='red', s=50, alpha=1)
    ax2.set_xlim([0, 1])
    ax2.set_ylim([0, 1])

    ax2.set_title('$(k_1, k_2, k_3)$ output space')
    # ax2.axis('equal')

    global SHOW_EQUILATERAL_TRIANGLE
    if SHOW_EQUILATERAL_TRIANGLE:
        ax2.plot([0, 0.5], [0, np.sqrt(3)/2], 'k--', alpha=0.5, linewidth=1)
        ax2.plot([1, 0.5], [0, np.sqrt(3)/2], 'k--', alpha=0.5, linewidth=1)
    


    points = np.array([
        (0, 0), # left
        (mod_k1, 0), # right
        (t*mu*mod_k1, t*mod_k1*np.sqrt(1-mu**2)) # top
    ])

    global K_LIST
    K_LIST = [
        *points
    ]

    triangle = Polygon(
        points,
        closed=True,
        edgecolor='black',
        facecolor='blueviolet',
        alpha=0.5,
        linewidth=1
    )
    ax2.add_patch(triangle)




    # Label sides
    ax2.text(*midpoint(points[0], points[1]), '$k_1$', ha='center', va='bottom', fontsize=12)
    ax2.text(*midpoint(points[0], points[2]), '$k_2$', ha='left', va='top', fontsize=12)
    ax2.text(*midpoint(points[1], points[2]), '$k_3$', ha='right', va='top', fontsize=12)

    # And angles
    # f"{angle:.01f}°"
    a1 = get_angle(points[1], points[0], points[2])
    a2 = get_angle(points[0], points[1], points[2])
    ax2.text(*points[0], f"{a1:0.1f}°", ha='right', va='bottom', fontsize=10)
    ax2.text(*points[1], f"{a2:0.1f}°", ha='left', va='bottom', fontsize=10)
    ax2.text(*points[2], f"{(180-a1-a2):0.1f}°", ha='center', va='bottom', fontsize=10)

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

def get_angle(p1, p2, p3):
    a = distance(p2, p3)
    b = distance(p1, p3)
    c = distance(p1, p2)
    return np.degrees(np.arccos((a**2 + c**2 - b**2) / (2 * a * c)))

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

def save_plot(event):
    extent = ax2.get_window_extent().transformed(ax2.figure.dpi_scale_trans.inverted())
    plt.savefig('ax2_figure.png', bbox_inches=extent)
    extent = ax1.get_window_extent().transformed(ax1.figure.dpi_scale_trans.inverted())
    plt.savefig('ax1_figure.png', bbox_inches=extent)
    



    # fig2, ax = plt.subplots(1, 1, figsize=(10,10))
    # global K_LIST
    # triangle = Polygon(
    #     K_LIST,
    #     closed=True,
    #     edgecolor='black',
    #     facecolor='pink',
    #     alpha=0.5,
    #     linewidth=1
    # )
    
    # ax.add_patch(triangle)

    # # Label sides and angle
    # ax.text(*midpoint(K_LIST[0], K_LIST[1]), '$k_1$', ha='center', va='bottom', fontsize=12)
    # ax.text(*midpoint(K_LIST[0], K_LIST[2]), '$k_2$', ha='left', va='top', fontsize=12)
    # ax.text(*midpoint(K_LIST[1], K_LIST[2]), '$k_3$', ha='right', va='top', fontsize=12)
    
    # ax.set_ylim(-0.5, 1)
    
    # ax.axis('equal')
    
    # extent = ax.get_window_extent().transformed(ax.figure.dpi_scale_trans.inverted())
    # plt.savefig('figure.png', bbox_inches=extent)

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

# Adding a button to save the plot
button_ax = plt.axes([0.8, 0.05, 0.1, 0.075])
button = Button(button_ax, 'Save Plot')
button.on_clicked(save_plot)

ax2.axis('equal')
refresh_ax1()

# Setting up button for t and mu input
plt.subplots_adjust(bottom=0.3)
text_box_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
text_box = TextBox(text_box_ax, 'Input comma separated $\mu$, t pair:', initial='')
text_box.on_submit(submit)


plt.show()
