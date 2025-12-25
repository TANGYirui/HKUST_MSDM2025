import io
import requests
import numpy as np
import pandas as pd
import networkx as nx
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
import os
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

# Ensure working directory is set to script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Set random seed for reproducibility in graph layout
np.random.seed(42)

# ==========================================
# 0. Configuration
# ==========================================
CONFIG = {
    'END_DATE': datetime.today().strftime('%Y-%m-%d'),
    'START_DATE': (datetime.today() - timedelta(days=365 * 7)).strftime('%Y-%m-%d'),

    'DATA_THRESH': 0.9,

    'WINDOW_SIZE': 252,
    'STEP': 21
}


# ==========================================
# 1. Data Acquisition Module
# ==========================================

def get_dow_tickers_and_sectors():

    print("\n[Phase 1] Initializing Dow Jones list...")

    # --- Strategy A: Scrape from Wikipedia ---
    url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"

    try:
        print("   -> Attempting to fetch list from Wikipedia...")
        dfs = pd.read_html(url)

        df = dfs[1]

        rename_map = {'Symbol': 'Symbol', 'Ticker': 'Symbol', 'Industry': 'GICS Sector'}
        df.rename(columns=rename_map, inplace=True)

        if 'Symbol' in df.columns and 'GICS Sector' in df.columns:
            tickers = df['Symbol'].tolist()
            sector_map = dict(zip(df['Symbol'], df['GICS Sector']))
            print(f"   -> Successfully retrieved {len(tickers)} Dow Jones constituents.")
            return tickers, sector_map
        else:
            raise ValueError("Wikipedia table format unexpected.")

    except Exception as e:
        print(f"   -> [Warning] Download failed ({e}). Switching to Backup Mode.")

        # --- Strategy B: Hardcoded Backup List (Updated 2024-2025) ---
        backup_data = {
            # Technology
            'AAPL': 'Information Technology', 'MSFT': 'Information Technology',
            'NVDA': 'Information Technology', 'IBM':  'Information Technology',
            'CRM':  'Information Technology', 'CSCO': 'Information Technology',

            # Financials
            'JPM': 'Financials', 'GS':  'Financials', 'V':   'Financials',
            'AXP': 'Financials', 'TRV': 'Financials',

            # Health Care
            'UNH':  'Health Care', 'JNJ':  'Health Care',
            'MRK':  'Health Care', 'AMGN': 'Health Care',

            # Consumer Discretionary
            'AMZN': 'Consumer Discretionary', 'HD':   'Consumer Discretionary',
            'MCD':  'Consumer Discretionary', 'NKE':  'Consumer Discretionary',

            # Consumer Staples
            'WMT': 'Consumer Staples', 'KO':  'Consumer Staples',
            'PG':  'Consumer Staples',

            # Industrials
            'CAT': 'Industrials', 'HON': 'Industrials',
            'BA':  'Industrials', 'MMM': 'Industrials',

            # Materials
            'SHW': 'Materials',

            # Energy
            'CVX': 'Energy',

            # Communication Services
            'VZ':  'Communication Services', 'DIS': 'Communication Services'
        }

        tickers = list(backup_data.keys())
        print(f"   -> Loaded {len(tickers)} stocks from backup list.")
        return tickers, backup_data


def get_sp500_tickers_and_sectors():
    print("\n[Phase 1] Initializing S&P 500 list...")

    # --- Strategy A: GitHub CSV ---
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    try:
        print("   -> Attempting to download S&P 500 list from GitHub...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

        if 'Symbol' not in df.columns:
            df.rename(columns={'Ticker': 'Symbol'}, inplace=True)

        df['Symbol'] = df['Symbol'].str.replace('.', '-', regex=False)

        tickers = df['Symbol'].tolist()
        sector_map = dict(zip(df['Symbol'], df['GICS Sector']))
        print(f"   -> Successfully retrieved {len(tickers)} stocks.")
        return tickers, sector_map

    except Exception as e:
        print(f"   -> [Warning] Download failed ({e}). Switching to Backup Mode.")

        # --- Strategy B: Hardcoded Backup List ---
        backup_data = {
            'AAPL': 'Information Technology', 'MSFT': 'Information Technology',
            'NVDA': 'Information Technology', 'IBM': 'Information Technology',
            'GOOG': 'Communication Services', 'META': 'Communication Services',
            'DIS': 'Communication Services',
            'AMZN': 'Consumer Discretionary', 'TSLA': 'Consumer Discretionary',
            'PG': 'Consumer Staples', 'KO': 'Consumer Staples',
            'XOM': 'Energy', 'CVX': 'Energy', 'SLB': 'Energy',
            'JPM': 'Financials', 'BAC': 'Financials', 'GS': 'Financials',
            'JNJ': 'Health Care', 'PFE': 'Health Care', 'LLY': 'Health Care',
            'GE': 'Industrials', 'BA': 'Industrials', 'CAT': 'Industrials'
        }
        return list(backup_data.keys()), backup_data


def fetch_and_process_data(tickers):
    print(f"\n[Phase 1] Downloading price data ({CONFIG['START_DATE']} to {CONFIG['END_DATE']})...")
    print("   -> Note: This may take 1-2 minutes depending on data volume...")

    raw_data = yf.download(tickers, start=CONFIG['START_DATE'], end=CONFIG['END_DATE'], progress=False)['Close']

    valid_data = raw_data.dropna(axis=1, thresh=int(raw_data.shape[0] * CONFIG['DATA_THRESH']))
    valid_data = valid_data.ffill().dropna()

    print(f"   -> Original count: {len(tickers)}, Valid count: {valid_data.shape[1]}")

    log_returns = np.log(valid_data / valid_data.shift(1)).dropna()

    return log_returns


# ==========================================
# 2. Core Algorithm Module
# ==========================================
def calculate_mst(log_returns):
    corr_matrix = log_returns.corr()

    dist_matrix = np.sqrt(2 * (1 - corr_matrix))
    dist_matrix = dist_matrix.fillna(0)
    dist_matrix[dist_matrix < 0] = 0

    G_full = nx.from_pandas_adjacency(dist_matrix)
    MST = nx.minimum_spanning_tree(G_full)

    return MST, dist_matrix, corr_matrix


# ==========================================
# 3. Visualization Module
# ==========================================
def plot_static_mst(MST, sector_map, index_name="S&P 500"):
    N = MST.number_of_nodes()
    print(f"\n[Phase 3] Generating MST Visualization ({index_name}, Nodes: {N})...")

    if N > 100:
        d_node_size = 20
        d_font_size = 4
        d_edge_width = 0.3
        d_alpha = 0.7
        d_k = 0.05
        print("   -> Large network detected. Switched to [Fine-grained Mode].")
    else:
        d_node_size = 400
        d_font_size = 10
        d_edge_width = 1.2
        d_alpha = 0.9
        d_k = 0.5
        print("   -> Small network detected. Switched to [Large-view Mode].")

    plt.figure(figsize=(10, 10))

    pos = nx.spring_layout(MST, k=d_k, iterations=100, seed=42)

    unique_sectors = list(set(sector_map.values()))
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_sectors)))
    sector_to_color = dict(zip(unique_sectors, colors))

    node_colors = []
    for node in MST.nodes():
        sec = sector_map.get(node, 'Unknown')
        node_colors.append(sector_to_color.get(sec, (0.5, 0.5, 0.5)))

    nx.draw_networkx_edges(MST, pos, alpha=0.4, width=d_edge_width, edge_color='gray')
    nx.draw_networkx_nodes(MST, pos, node_size=d_node_size, node_color=node_colors, alpha=d_alpha)
    nx.draw_networkx_labels(MST, pos, font_size=d_font_size, font_family="sans-serif")

    legend_patches = [mpatches.Patch(color=col, label=sec) for sec, col in sector_to_color.items()]
    plt.legend(handles=legend_patches, title="GICS Sectors", loc="upper left", bbox_to_anchor=(1, 1))

    plt.title(f"{index_name} Minimum Spanning Tree\nMetric: $d(i,j) = \\sqrt{{2(1-\\rho_{{ij}})}}$", fontsize=20)
    plt.axis('off')

    safe_name = index_name.replace(" ", "_").lower()
    filename = f"{safe_name}_mst_static.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   -> Chart saved: {filename}")
    plt.show()


# ==========================================
# 4. Visualization Module: Dendrogram
# ==========================================
def plot_hierarchical_tree(dist_matrix, index_name="S&P 500"):
    print(f"\n[Phase 4] Generating Hierarchical Tree / Dendrogram ({index_name})...")

    condensed_dist = squareform(dist_matrix.values)

    Z = linkage(condensed_dist, method='single')

    plt.figure(figsize=(25, 12))

    dendrogram(
        Z,
        labels=dist_matrix.index,
        leaf_rotation=90,
        leaf_font_size=8 if len(dist_matrix) > 100 else 12,
        color_threshold=0  # Optional: color clusters
    )

    plt.title(f"{index_name} Hierarchical Tree (Dendrogram)\nMethod: Single Linkage (Equivalent to MST)", fontsize=18)
    plt.ylabel(f"Ultrametric Distance $d(i,j)$")
    plt.xlabel("Stocks")

    safe_name = index_name.replace(" ", "_").lower()
    filename = f"{safe_name}_dendrogram.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   -> Dendrogram saved: {filename}")
    plt.show()

# ==========================================
# 5. Dynamic Analysis Module (Bonus)
# ==========================================
def run_dynamic_analysis(log_returns, index_name="S&P 500"):
    print(f"\n[Bonus] Starting Dynamic MST Analysis ({index_name})...")

    window = CONFIG['WINDOW_SIZE']
    step = CONFIG['STEP']
    all_dates = log_returns.index

    dates = []
    tree_lengths = []
    avg_correlations = []

    for i in range(0, len(all_dates) - window, step):
        current_dates = all_dates[i: i + window]
        subset = log_returns.loc[current_dates]

        MST_sub, _, corr_sub = calculate_mst(subset)

        total_weight = MST_sub.size(weight="weight")
        if MST_sub.number_of_nodes() > 1:
            ntl = total_weight / (MST_sub.number_of_nodes() - 1)
        else:
            ntl = 0

        avg_corr = corr_sub.values[np.triu_indices_from(corr_sub.values, k=1)].mean()

        dates.append(current_dates[-1])
        tree_lengths.append(ntl)
        avg_correlations.append(avg_corr)

    plot_dynamic_trend(dates, tree_lengths, avg_correlations, index_name)

    if len(tree_lengths) > 0:
        min_idx = np.argmin(tree_lengths)
        return dates[min_idx]
    else:
        return None


def plot_dynamic_trend(dates, lengths, corrs, index_name):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('MST Normalized Length (Risk Metric)', color=color, fontsize=12)
    ax1.plot(dates, lengths, color=color, linewidth=2, label='MST Length')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Average Correlation', color=color, fontsize=12)
    ax2.plot(dates, corrs, color=color, linestyle='--', alpha=0.6, label='Avg Correlation')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f"{index_name} Dynamic Market Structure: MST Length vs Correlation", fontsize=14)

    safe_name = index_name.replace(" ", "_").lower()
    filename = f"{safe_name}_mst_dynamic_trend.png"

    plt.savefig(filename, dpi=300)
    print(f"   -> Trend chart saved: {filename}")
    plt.show()


# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    # --- Phase 1: Data Preparation ---
    # 1. S&P 500
    tickers_sp, sector_map_sp = get_sp500_tickers_and_sectors()
    log_returns_sp = fetch_and_process_data(tickers_sp)

    # 2. Dow Jones
    tickers_dow, sector_map_dow = get_dow_tickers_and_sectors()
    log_returns_dow = fetch_and_process_data(tickers_dow)

    # --- Phase 2: Full MST Calculation ---
    print("\n[Phase 2] Calculating MST for full time range...")

    mst_sp, dist_matrix_sp, _ = calculate_mst(log_returns_sp)
    mst_dow, dist_matrix_dow, _ = calculate_mst(log_returns_dow)

    # --- Phase 3: Visualization ---
    plot_static_mst(mst_sp, sector_map_sp, index_name="S&P 500")
    plot_static_mst(mst_dow, sector_map_dow, index_name="Dow Jones")

    plot_hierarchical_tree(dist_matrix_sp, index_name="S&P 500")
    plot_hierarchical_tree(dist_matrix_dow, index_name="Dow Jones")


    stress_date_sp = run_dynamic_analysis(log_returns_sp, index_name="S&P 500")
    stress_date_dow = run_dynamic_analysis(log_returns_dow, index_name="Dow Jones")

    print("\n[Results Summary]")
    if stress_date_sp:
         print(f"S&P 500 Max Stress Date: {stress_date_sp.date()}")
    if stress_date_dow:
         print(f"Dow Jones Max Stress Date: {stress_date_dow.date()}")