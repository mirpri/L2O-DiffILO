# Gurobi-only testing script for baseline comparisons
import os
import json
from datetime import datetime

import hydra
from omegaconf import DictConfig
from tqdm import tqdm
import gurobipy as gp

from src.utils import set_seed, set_cpu_num
import src.tb_writter as tb_writter


@hydra.main(version_base=None, config_path="config", config_name="test")
def test_gurobi_only(config: DictConfig):
    # Basic setup
    set_seed(config.seed)
    set_cpu_num(config.num_workers + 1)

    # Create a baseline-specific output directory (independent of model_dir)
    now = datetime.now()
    test_dir = os.path.join(
        "./workspace/baseline",
        config.dataset.name,
        "test",
        now.strftime("%m-%d"),
        f"{now.strftime('%H:%M:%S')}-{config.job_name}-gurobi",
    )
    log_dir = os.path.join(test_dir, "logs")
    json_dir = os.path.join(test_dir, "jsons")
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)
    tb_writter.set_logger(test_dir)

    # Collect .lp files
    data_dir = config.paths.test_data_dir
    files = sorted(f for f in os.listdir(data_dir) if f.endswith(".lp"))

    # Global console logging similar to test.py
    try:
        gp.setParam("LogToConsole", 1)
    except gp.GurobiError:
        pass  # ignore if environment not initialized yet

    for fname in tqdm(files, desc="Solving (Gurobi only)"):
        ins_path = os.path.join(data_dir, fname)
        try:
            m = gp.read(ins_path)
            # Match parameters used in test.py
            m.Params.TimeLimit = 1000
            m.Params.Threads = 1
            m.Params.MIPFocus = 1
            m.Params.LogFile = os.path.join(log_dir, f"{fname}.gurobi.log")

            m.optimize()

            result = {
                "obj": m.ObjVal if m.SolCount > 0 else None,
                "time": m.Runtime,
                "nnodes": m.NodeCount,
                "gap": getattr(m, "MIPGap", None),
                "stat": m.status,
                "approach": "gurobi",
            }
            print(result)
        except gp.GurobiError as e:
            result = {
                "obj": None,
                "time": None,
                "nnodes": None,
                "gap": None,
                "stat": "error",
                "error": str(e),
                "approach": "gurobi",
            }
            print(f"Gurobi error on {fname}: {e}")
        except Exception as e:
            result = {
                "obj": None,
                "time": None,
                "nnodes": None,
                "gap": None,
                "stat": "error",
                "error": str(e),
                "approach": "gurobi",
            }
            print(f"Unexpected error on {fname}: {e}")

        # Write per-instance JSON
        json_path = os.path.join(json_dir, f"{fname}.gurobi.json")
        with open(json_path, "w") as f:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    test_gurobi_only()