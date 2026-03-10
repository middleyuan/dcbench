import sys
from pathlib import Path

# Add the local domino implementation to the path
# The path is relative to the dcbench root (../../sdbench/postprocessors/domino)
domino_path = (
    Path(__file__).resolve().parents[3] / ".." / ".." / "sdbench" / "postprocessors"
).resolve()
sys.path.insert(0, str(domino_path))

import dcbench
from domino import SpotlightSlicer, embed, DominoSlicer

from dcbench.tasks.slice_discovery.run import run_sdms

if __name__ == "__main__":

    task = dcbench.tasks["slice_discovery"]
    problems = [p for p in task.problems.values() if p.attributes["dataset"] == "imagenet"]

    # for weight in [1,2,3,5,7,10,20,50]:
    for weight in [10]:
        solutions, metrics = run_sdms(
            problems,
            slicer_class=DominoSlicer,
            slicer_config=dict(
                y_hat_log_likelihood_weight=weight,
                y_log_likelihood_weight=weight,
            ),
            encoder="clip",
            num_workers=10
        )

    # solutions, metrics = run_sdms(
    #     list(task.problems.values()),
    #     slicer_class=SpotlightSlicer,
    #     slicer_config=dict(
    #         # y_hat_log_likelihood_weight=10,
    #         # y_log_likelihood_weight=10,
    #         n_steps=100,
    #     ),
    #     encoder="clip",
    #     num_workers=0
    # )
