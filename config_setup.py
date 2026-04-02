#!/usr/bin/env python3
import os
import argparse
import yaml
import pathlib

def setup_dcbench(target_dir, sdbench_dir=None):
    # 1. Create the .dcbench directory
    target_path = pathlib.Path(target_dir).resolve()
    print(f"[*] Setting up .dcbench directory at: {target_path}")
    target_path.mkdir(parents=True, exist_ok=True)

    # 2. Create the configuration file
    config_file = target_path / "dcbench-config.yaml"
    config = {
        "local_dir": str(target_path),
        "public_bucket_name": "dcbench",
        "hidden_bucket_name": "dcbench-hidden",
        "celeba_dir": str(target_path / "datasets" / "celeba"),
        "imagenet_dir": str(target_path / "datasets" / "imagenet")
    }

    with open(config_file, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"[*] Created configuration file: {config_file}")

    # 3. Create datasets directory
    datasets_dir = target_path / "datasets"
    datasets_dir.mkdir(parents=True, exist_ok=True)

    # 4. Linking datasets from SDBench if provided
    if sdbench_dir:
        sdbench_path = pathlib.Path(sdbench_dir).resolve()
        base_dataset_path = sdbench_path / "data" / "base_dataset"
        
        for dataset in ["imagenet", "celeba"]:
            src = base_dataset_path / dataset
            dst = datasets_dir / dataset
            
            if src.exists():
                if dst.exists() or dst.is_symlink():
                    print(f"[!] Target {dst} already exists, skipping...")
                else:
                    try:
                        dst.symlink_to(src)
                        print(f"[*] Created symlink: {dst} -> {src}")
                    except OSError as e:
                        print(f"[!] Error creating symlink for {dataset}: {e}")
            else:
                print(f"[!] Source dataset not found at: {src}")

    print("\n[✔] Setup complete!")
    print("\nTo use this configuration, set the following environment variable:")
    print(f"export DCBENCH_CONFIG=\"{config_file}\"")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup dcbench configuration and link SDBench datasets.")
    parser.add_argument("target_dir", help="Where to create the .dcbench directory.")
    parser.add_argument("--sdbench_dir", help="Path to SDBench root directory to link datasets from.", default="../../")
    
    args = parser.parse_args()
    setup_dcbench(args.target_dir, args.sdbench_dir)
