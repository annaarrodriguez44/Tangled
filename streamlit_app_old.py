# app.py
import streamlit as st
import pandas as pd
import numpy as np
import itertools
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Yarn Material Analysis", layout="wide")

st.title("🧶 Yarn Material Pair Analysis Dashboard")

# --- Upload Excel file ---
st.sidebar.header("1️⃣ Load Excel File")
uploaded = st.sidebar.file_uploader("Upload your Database_YARN.xlsx", type=["xlsx"])

if uploaded is not None:
    df = pd.read_excel(uploaded)

    st.sidebar.success("File loaded successfully ✅")

    # --- Select key columns ---
    st.sidebar.header("2️⃣ Select column names")
    all_cols = df.columns.tolist()

    name_col = st.sidebar.selectbox("Name column", options=all_cols)
    price_col = st.sidebar.selectbox("Price column", options=all_cols)
    thickness_col = st.sidebar.selectbox("Thickness / Yarn weight column", options=[None] + all_cols)
    color_col = st.sidebar.selectbox("Color column", options=[None] + all_cols)

    # composition columns (fibres)
    st.sidebar.markdown("### Composition columns")
    comp_cols = st.sidebar.multiselect("Select fibre/material columns", options=all_cols)

    if not comp_cols:
        st.warning("Please select at least one composition column.")
        st.stop()

    # --- Prepare binary DataFrame (1 if fibre present) ---
    df_binary = df[comp_cols].copy()
    for c in comp_cols:
        df_binary[c] = pd.to_numeric(df_binary[c], errors='coerce').fillna(0)
        df_binary[c] = (df_binary[c] > 0).astype(int)

    st.markdown("### Material presence table (1 = present)")
    st.dataframe(df_binary.head(10))

    # ---------------------------
    # Compute pair statistics
    # ---------------------------
    def compute_pair_stats(df, df_binary, comp_cols, price_col=None, thickness_col=None):
        pair_rows = []
        cols = df_binary.columns.tolist()
        for a, b in itertools.combinations(cols, 2):
            mask = (df_binary[a] == 1) & (df_binary[b] == 1)
            cnt = int(mask.sum())
            if cnt == 0:
                pair_rows.append({
                    "pair": f"{a} + {b}",
                    "count": 0,
                    "mean_price": np.nan,
                    "median_thickness": np.nan
                })
                continue
            mean_price = np.nan
            median_th = np.nan
            if price_col and price_col in df.columns:
                mean_price = float(pd.to_numeric(df.loc[mask, price_col], errors='coerce').dropna().mean() or np.nan)
            if thickness_col and thickness_col in df.columns:
                median_th = float(pd.to_numeric(df.loc[mask, thickness_col], errors='coerce').dropna().median() or np.nan)
            pair_rows.append({
                "pair": f"{a} + {b}",
                "count": cnt,
                "mean_price": mean_price,
                "median_thickness": median_th
            })
        pairs_df = pd.DataFrame(pair_rows).sort_values("count", ascending=False).reset_index(drop=True)
        return pairs_df

    # ---------------------------
    # Show panels
    # ---------------------------
    st.markdown("## 📊 Material Pair Frequency & Stats")
    pairs_df = compute_pair_stats(df, df_binary, comp_cols, price_col=price_col, thickness_col=thickness_col)

    cols = st.columns([2, 1])
    with cols[0]:
        st.write("Top pairs (by co-occurrence)")
        st.dataframe(pairs_df.head(20).reset_index(drop=True))

        fig_bar = go.Figure()
        topn = pairs_df.head(15)
        fig_bar.add_trace(go.Bar(x=topn["pair"], y=topn["count"], name="count", marker_color="teal"))
        fig_bar.update_layout(title="Top material pairs (count)", xaxis_tickangle=-45, height=420, margin=dict(t=40))
        st.plotly_chart(fig_bar, use_container_width=True)

    with cols[1]:
        st.write("Least frequent pairs (including zero)")
        st.dataframe(pairs_df.tail(20).sort_values("count").reset_index(drop=True))
        bottomn = pairs_df.tail(15).sort_values("count")
        fig_bar2 = go.Figure()
        fig_bar2.add_trace(go.Bar(x=bottomn["pair"], y=bottomn["count"], name="count", marker_color="lightgray"))
        fig_bar2.update_layout(title="Least frequent material pairs", xaxis_tickangle=-45, height=420, margin=dict(t=40))
        st.plotly_chart(fig_bar2, use_container_width=True)

    # ---------------------------
    # Pair detail section
    # ---------------------------
    st.markdown("## 🧮 Pair price / thickness comparison")
    sel_pair = st.selectbox("Select a pair to inspect", options=pairs_df["pair"].tolist(), index=0)
    if sel_pair:
        a, b = [s.strip() for s in sel_pair.split("+")]
        mask = (df_binary[a] == 1) & (df_binary[b] == 1)
        sample = df.loc[mask].copy()
        st.write(f"Products with {sel_pair}: {len(sample)}")
        if not sample.empty:
            cols_show = [c for c in [name_col, price_col, thickness_col, color_col] + comp_cols if c in sample.columns]
            st.dataframe(sample[cols_show].head(50))

            if price_col and thickness_col and price_col in sample.columns and thickness_col in sample.columns:
                s = sample.copy()
                s[price_col] = pd.to_numeric(s[price_col], errors='coerce')
                s[thickness_col] = pd.to_numeric(s[thickness_col], errors='coerce')
                fig = px.scatter(
                    s,
                    x=thickness_col,
                    y=price_col,
                    hover_data=[name_col, color_col] if name_col and color_col else [name_col],
                    title=f"Price vs Thickness for {sel_pair}",
                    color_discrete_sequence=["purple"]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Price or thickness column missing for scatter.")

    # ---------------------------
    # Network visualization
    # ---------------------------
    st.markdown("## 🕸️ Material co-occurrence network")
    G = nx.Graph()
    for _, row in pairs_df.iterrows():
        a, b = [s.strip() for s in row["pair"].split("+")]
        cnt = int(row["count"])
        if cnt > 0:
            G.add_node(a, size=int(df_binary[a].sum()))
            G.add_node(b, size=int(df_binary[b].sum()))
            G.add_edge(a, b, weight=cnt)

    if len(G.nodes) > 0:
        pos = nx.spring_layout(G, seed=42, k=0.6)
        edge_x, edge_y = [], []
        for u, v in G.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        node_x, node_y, node_text, node_size = [], [], [], []
        for n, data in G.nodes(data=True):
            x, y = pos[n]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"{n} ({int(data.get('size', 0))})")
            node_size.append(max(8, int(data.get('size', 0)) * 3))

        edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color="#888"),
                                hoverinfo="none", mode="lines")
        node_trace = go.Scatter(x=node_x, y=node_y, mode="markers+text", hoverinfo="text",
                                textposition="top center",
                                marker=dict(showscale=False, color="skyblue", size=node_size, line_width=1),
                                text=node_text)

        fig_net = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(title="Material co-occurrence network (edge weight = count)",
                                             showlegend=False, hovermode="closest",
                                             margin=dict(b=20, l=5, r=5, t=40)))
        st.plotly_chart(fig_net, use_container_width=True)
    else:
        st.info("Not enough co-occurrence data to build network.")
else:
    st.info("👈 Upload your Excel file in the sidebar to start.")
