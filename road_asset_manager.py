"""
road_asset_manager.py - Gestion de activos viales municipales Colombia
Esquema compatible con INVIAS y PCI (ASTM D6433)
Uso: python road_asset_manager.py --accion demo
"""
import argparse, csv, json, sys
from datetime import datetime

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Instala: pip install pandas matplotlib numpy")
    sys.exit(1)

PCI_CLASIFICACION = {
    (85,100):("Excelente","#2ECC71"), (70,84):("Muy bueno","#27AE60"),
    (55,69):("Bueno","#F1C40F"),     (40,54):("Regular","#E67E22"),
    (25,39):("Malo","#E74C3C"),      (10,24):("Muy malo","#C0392B"),
    (0,9):("Fallado","#7B241C"),
}
COSTOS = {
    "Excelente":0,"Muy bueno":0,"Bueno":50000,
    "Regular":150000,"Malo":350000,"Muy malo":600000,"Fallado":1200000,
}

def clasificar(pci):
    for (mn,mx),(cl,co) in PCI_CLASIFICACION.items():
        if mn<=int(pci)<=mx: return cl, co
    return "Sin datos","#AAAAAA"

def demo():
    datos = [
        ["AV-001","Av. El Poblado","Primaria","Asfalto",2800,14,72,"Medellín"],
        ["AV-002","Cl 10","Secundaria","Asfalto",1200,9,45,"Medellín"],
        ["AV-003","Kr 43","Secundaria","Concreto",1800,11,88,"Medellín"],
        ["AV-004","Cll 30","Terciaria","Afirmado",600,6,22,"Bello"],
        ["AV-005","Av. Guayabal","Primaria","Asfalto",3200,16,61,"Medellín"],
        ["AV-006","Cll 65","Secundaria","Asfalto",1500,10,38,"Medellín"],
        ["AV-007","Via Guarne","Terciaria","Afirmado",900,6,15,"Guarne"],
        ["AV-008","Av. Las Vegas","Primaria","Asfalto",2100,14,79,"Medellín"],
        ["AV-009","Cll 44","Secundaria","Concreto",1100,9,55,"Envigado"],
        ["AV-010","Via Copacabana","Terciaria","Afirmado",750,5,8,"Copacabana"],
    ]
    cols = ["id","nombre","tipo","material","longitud_m","ancho_m","pci","municipio"]
    df = pd.DataFrame(datos, columns=cols)
    df.to_csv("activos_demo.csv", index=False)
    print("Demo creado: activos_demo.csv")
    return df

def reporte(df):
    df["estado"] = df["pci"].apply(lambda x: clasificar(x)[0])
    df["area_m2"] = df["longitud_m"] * df["ancho_m"]
    df["costo"] = df.apply(lambda r: COSTOS.get(r["estado"],0)*r["area_m2"], axis=1)
    print("\n=== REPORTE MALLA VIAL ===")
    print(f"Total activos:     {len(df)}")
    print(f"Longitud total:    {df['longitud_m'].sum()/1000:.2f} km")
    print(f"PCI promedio:      {df['pci'].mean():.1f}")
    print(f"Costo intervencion: ${df['costo'].sum():,.0f} COP")
    print(f"Atencion urgente:  {(df['pci']<25).sum()} activos")
    print("\nPor estado:")
    for e, g in df.groupby("estado"):
        print(f"  {e}: {len(g)} activos")

def visualizar(df):
    df["estado"] = df["pci"].apply(lambda x: clasificar(x)[0])
    colores = {cl:co for (_,__),(cl,co) in PCI_CLASIFICACION.items()}
    fig, axes = plt.subplots(1,2,figsize=(14,5))
    fig.suptitle("Estado Malla Vial Municipal", fontsize=13, fontweight="bold")
    cnt = df["estado"].value_counts()
    axes[0].bar(cnt.index, cnt.values,
                color=[colores.get(e,"#AAA") for e in cnt.index])
    axes[0].set_title("Activos por Estado")
    axes[0].tick_params(axis="x", rotation=30)
    axes[1].hist(df["pci"], bins=8, color="#3498DB", edgecolor="white")
    axes[1].axvline(df["pci"].mean(), color="red", linestyle="--",
                    label=f"Promedio: {df['pci'].mean():.0f}")
    axes[1].set_title("Distribucion PCI")
    axes[1].set_xlabel("PCI (0-100)")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig("dashboard_vial.png", dpi=150)
    print("Dashboard guardado: dashboard_vial.png")
    plt.show()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--accion", choices=["demo","reporte","visualizar"], required=True)
    p.add_argument("--input")
    args = p.parse_args()
    if args.accion == "demo":
        df = demo(); reporte(df); visualizar(df)
    else:
        if not args.input: print("--input requerido"); sys.exit(1)
        df = pd.read_csv(args.input)
        if args.accion == "reporte": reporte(df)
        elif args.accion == "visualizar": visualizar(df)

if __name__ == "__main__":
    main()
