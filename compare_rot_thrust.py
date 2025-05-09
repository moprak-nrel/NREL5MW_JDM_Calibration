import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ruamel.yaml import YAML


ref_df = pd.read_csv(
    "./NREL_Reference_5MW_126.csv", usecols=["Wind Speed [m/s]", "Thrust [kN]", "Ct [-]"]
)
ref_df.rename(
    columns={"Wind Speed [m/s]": "WindSpeed", "Thrust [kN]": "RotThrust", "Ct [-]": "Ct"}, inplace=True
)
ref_df.set_index("WindSpeed", inplace=True)
RotThrust_df = pd.read_csv("./RotThrusts.csv", index_col="WindSpeed")
density = 1.225
D = 126
rotor_area = np.pi * D**2 /4.0
Ct_computed = 2 * RotThrust_df.RotThrust/(density * rotor_area * RotThrust_df.index**2) * 1000
RotThrust_df["Ct"] = Ct_computed
RotThrust_df.to_csv('OpenFAST_Ct.csv')


rt_computed = ref_df.Ct * density * rotor_area * ref_df.index**2 / 2.0 / 1e3

fig, axs = plt.subplots(nrows=2, sharex=True)
axs[0].plot(
    RotThrust_df.index, RotThrust_df.RotThrust, label="OpenFAST", color="red"
)
axs[0].plot(ref_df.index, rt_computed, label="Reference (computed)", color="b", ls ='dashed')
axs[0].plot(ref_df.index, ref_df.RotThrust, label="Reference", color="k", ls ='dotted')
axs[0].legend()
axs[0].set_ylabel("RotThrust [kN]")

axs[1].plot(RotThrust_df.index, Ct_computed, label="OpenFAST (computed)", color="red")
axs[1].plot(ref_df.index, ref_df.Ct, label="Reference", color="k", ls = 'dotted')
axs[1].legend()
axs[1].set_ylabel("Ct")
axs[1].set_xlabel("Wind Speed")
fig.suptitle("NREL 5MW Turbine")
plt.savefig("RotThrust.pdf", bbox_inches="tight")
