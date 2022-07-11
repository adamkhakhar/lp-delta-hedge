import os
import sys

sys.path.append(
    f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/utils/"
)
import image_creation

PATH_TO_RESULTS = (
    f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/results"
)
IL = lambda x: 2 * (x + 1) ** 0.5 / (x + 2) - 1
image_creation.create_plot_from_fn(
    IL,
    -1,
    1,
    y_min=None,
    y_max=None,
    save_path=PATH_TO_RESULTS,
    save_title="IL",
    xlabel=r"$\delta$",
    ylabel="Impremanent Loss",
    title="Impermanent Loss",
)
