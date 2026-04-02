import os
import dcbench
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

def get_stats(force_refresh=False):
    save_path = ".dcbench/slice_discovery_stats.csv"
    if not force_refresh and os.path.exists(save_path):
        print(f"[*] Loading cached stats from {save_path}")
        return pd.read_csv(save_path)

    task = dcbench.tasks["slice_discovery"]
    problems = task.problems
    
    results = []
    
    for problem_id, problem in tqdm(problems.items(), desc="Processing problems"):
        category = problem.attributes["slice_category"]
        
        # Load test predictions
        test_preds = problem["test_predictions"]
        y_true = test_preds["target"].to_numpy()
        y_prob = test_preds["probs"].to_numpy()
        
        if y_prob.ndim == 2 and y_prob.shape[1] == 2:
            y_pred = (y_prob[:, 1] > 0.5).astype(int)
        else:
            y_pred = (y_prob > 0.5).astype(int)
            
        is_correct = (y_pred == y_true)
        overall_acc = is_correct.mean()
        
        # Load test slices
        test_slices = problem["test_slices"]
        slices = test_slices["slices"].to_numpy()
        
        num_slices = slices.shape[1]
        total_dataset_size = len(y_true)
        
        slice_accs = []
        slice_sizes = []
        for i in range(num_slices):
            mask = (slices[:, i] == 1)
            slice_sizes.append(mask.sum())
            if mask.any():
                slice_acc = is_correct[mask].mean()
                slice_accs.append(slice_acc)
        
        # Filter "error slices" (accuracy lower than overall accuracy)
        error_slice_accs = [acc for acc in slice_accs if acc < overall_acc]
        
        avg_slice_acc = np.mean(slice_accs) if slice_accs else np.nan
        avg_slice_size = np.mean(slice_sizes) if slice_sizes else 0
        avg_error_slice_acc = np.mean(error_slice_accs) if error_slice_accs else np.nan
        min_slice_acc = np.min(slice_accs) if slice_accs else np.nan
        
        results.append({
            "problem_id": problem_id,
            "category": category,
            "overall_acc": overall_acc,
            "avg_slice_acc": avg_slice_acc,
            "avg_error_slice_acc": avg_error_slice_acc,
            "min_slice_acc": min_slice_acc,
            "avg_degradation": overall_acc - avg_slice_acc if not np.isnan(avg_slice_acc) else 0,
            "max_degradation": overall_acc - min_slice_acc if not np.isnan(min_slice_acc) else 0,
            "num_slices": num_slices,
            "num_error_slices": len(error_slice_accs),
            "total_dataset_size": total_dataset_size,
            "avg_slice_size": avg_slice_size,
        })
        
    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"[*] Stats saved to {save_path}")
    return df

def plot_stats(df):
    plt.figure(figsize=(15, 10))
    
    # 1. Distribution of Accuracy Degradation by Category
    plt.subplot(2, 2, 1)
    sns.boxplot(x='category', y='avg_degradation', data=df)
    plt.title('Accuracy Degradation (Overall - Avg Slice) by Category')
    plt.xticks(rotation=45)
    
    # 2. Number of Error Slices vs Total Slices
    plt.subplot(2, 2, 2)
    category_counts = df.groupby('category')[['num_slices', 'num_error_slices']].mean()
    category_counts.plot(kind='bar', ax=plt.gca())
    plt.title('Avg Number of Slices vs. Error Slices')
    plt.xticks(rotation=45)
    
    # 3. Overall Accuracy vs. Min Slice Accuracy
    plt.subplot(2, 2, 3)
    for cat in df['category'].unique():
        cat_df = df[df['category'] == cat]
        plt.scatter(cat_df['overall_acc'], cat_df['min_slice_acc'], label=cat, alpha=0.6)
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlabel('Overall Accuracy')
    plt.ylabel('Min Slice Accuracy')
    plt.title('Overall vs. Worst-performing Slice Accuracy')
    plt.legend()
    
    # 4. Average slice size vs. total dataset size
    plt.subplot(2, 2, 4)
    size_comparison = df.groupby('category')[['total_dataset_size', 'avg_slice_size']].mean()
    size_comparison.plot(kind='bar', ax=plt.gca(), logy=True)
    plt.title('Avg Slice Size vs. Total Dataset Size by Category')
    plt.ylabel('Average Size (log scale)')
    
    plt.tight_layout()
    plot_path = ".dcbench/slice_discovery_plots.png"
    plt.savefig(plot_path)
    print(f"[*] Plots saved to {plot_path}")
    plt.show()

if __name__ == "__main__":
    df = get_stats()
    
    print("\nSummary Statistics by Category:")
    summary = df.groupby("category").agg({
        "problem_id": "count",
        "num_slices": "mean",
        "num_error_slices": "mean",
        "overall_acc": "mean",
        "avg_error_slice_acc": "mean",
        "avg_degradation": "mean",
        "total_dataset_size": "mean",
        "avg_slice_size": "mean",
    }).rename(columns={"problem_id": "num_problems"})
    
    print(summary)
    plot_stats(df)