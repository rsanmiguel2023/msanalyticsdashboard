import matplotlib.pyplot as plt

def simple_line(df, x, y, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df[x], df[y])
    ax.set_title(title)
    return fig
