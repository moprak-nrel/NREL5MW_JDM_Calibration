import matplotlib.pyplot as plt
import pandas as pd

Ct_df = pd.read_csv(
    "./NREL_Reference_5MW_126.csv", usecols=["Wind Speed [m/s]", "Ct [-]"]
)
Ct_df.rename(columns={"Wind Speed [m/s]": "WindSpeed", "Ct [-]": "Ct"}, inplace=True)
Ct_df.set_index("WindSpeed", inplace=True)
RotSpeed_df = pd.read_csv("./RotSpeeds.csv", index_col="WindSpeed")
combined_df = Ct_df.join(RotSpeed_df, how="outer", sort=True).interpolate("cubic")

fig, axs = plt.subplots(nrows=2, sharex=True)
axs[0].plot(Ct_df.index, Ct_df.Ct, label="Original", color="k")
axs[0].plot(combined_df.index, combined_df.Ct, label="Interpolated", ls="dotted")
axs[0].legend()
axs[0].set_ylabel("Ct")

axs[1].plot(RotSpeed_df.index, RotSpeed_df.RotSpeed, label="Original", color="k")
axs[1].plot(combined_df.index, combined_df.RotSpeed, label="Interpolated", ls="dotted")
axs[1].legend()
axs[1].set_xlabel("Wind Speed")
axs[1].set_ylabel("RotSpeed (rpm)")
fig.suptitle("NREL 5MW Turbine")
plt.savefig("ct_rotspeed.pdf", bbox_inches="tight")
