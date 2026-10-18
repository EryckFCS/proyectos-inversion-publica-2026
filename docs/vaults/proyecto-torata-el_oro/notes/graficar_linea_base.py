import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

vault_dir = 'd:/07_Ciclo/septimo_ciclo/public_investment_projects/docs/vaults/proyecto-torata-el_oro'
csv_path = f'{vault_dir}/notes/linea_base.csv'
asset_dir = f'{vault_dir}/asset'
os.makedirs(asset_dir, exist_ok=True)

df = pd.read_csv(csv_path)

# 1. Gráfico Servicios Básicos
df_serv = df[df['panel'] == 'servicios'].sort_values(by='valor', ascending=True)
fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
bars = ax.barh(df_serv['etiqueta'], df_serv['valor'], color=['#c0392b' if x < 50 else '#2980b9' for x in df_serv['valor']], height=0.6)
ax.set_xlim(0, 105)
ax.set_xlabel('Porcentaje de Viviendas (%)', fontsize=9, fontweight='bold')
ax.set_title('Acceso a Servicios Básicos y Brecha Sanitaria en Torata (2022)', fontsize=10, fontweight='bold', pad=12)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', fontsize=8.5, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{asset_dir}/grafico_servicios_torata.png', dpi=300)
plt.close()

# 2. Gráfico Comparativo Pobreza NBI
df_nbi = df[df['panel'] == 'nbi'].sort_values(by='valor', ascending=True)
fig, ax = plt.subplots(figsize=(7, 3.8), dpi=300)
colors = ['#27ae60', '#2980b9', '#f39c12', '#c0392b']
bars = ax.barh(df_nbi['etiqueta'], df_nbi['valor'], color=colors, height=0.55)
ax.set_xlim(0, 80)
ax.set_xlabel('Tasa de Pobreza por NBI (%)', fontsize=9, fontweight='bold')
ax.set_title('Brecha Territorial de Pobreza por NBI: Torata vs Comparadores', fontsize=10, fontweight='bold', pad=12)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 1.0, bar.get_y() + bar.get_height()/2, f'{w:.1f}%', va='center', fontsize=8.5, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{asset_dir}/grafico_nbi_torata.png', dpi=300)
plt.close()

# 3. Gráfico Uso del Suelo
df_suelo = df[df['panel'] == 'suelo']
fig, ax = plt.subplots(figsize=(6.5, 4), dpi=300)
wedges, texts, autotexts = ax.pie(
    df_suelo['valor'],
    labels=df_suelo['etiqueta'],
    autopct='%1.1f%%',
    startangle=140,
    colors=['#e67e22', '#27ae60', '#f1c40f', '#95a5a6'],
    wedgeprops=dict(width=0.6, edgecolor='w')
)
for at in autotexts:
    at.set_fontsize(8.5)
    at.set_fontweight('bold')
for t in texts:
    t.set_fontsize(8)
ax.set_title('Distribución del Uso y Aptitud del Suelo en Torata (8.538 ha)', fontsize=10, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig(f'{asset_dir}/grafico_suelo_torata.png', dpi=300)
plt.close()

# Sincronizar en _site
site_asset_dir = 'd:/07_Ciclo/septimo_ciclo/public_investment_projects/_site/docs/vaults/proyecto-torata-el_oro/asset'
os.makedirs(site_asset_dir, exist_ok=True)
import shutil
for g in ['grafico_servicios_torata.png', 'grafico_nbi_torata.png', 'grafico_suelo_torata.png']:
    shutil.copy2(f'{asset_dir}/{g}', f'{site_asset_dir}/{g}')

print("Gráficos de línea base generados y sincronizados.")
