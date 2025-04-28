import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ruamel.yaml import YAML


def get_ct_rotspeed(plot_interpolation=False):
    Ct_df = pd.read_csv(
        "./NREL_Reference_5MW_126.csv", usecols=["Wind Speed [m/s]", "Ct [-]"]
    )
    Ct_df.rename(
        columns={"Wind Speed [m/s]": "WindSpeed", "Ct [-]": "Ct"}, inplace=True
    )
    Ct_df.set_index("WindSpeed", inplace=True)
    RotSpeed_df = pd.read_csv("./RotSpeeds.csv", index_col="WindSpeed")
    combined_df = Ct_df.join(RotSpeed_df, how="outer", sort=True).interpolate("cubic")

    # Zero padding for cut-in and cut-out speeds
    for loc in [0.0, 2.9, 25.1, 50]:
        combined_df.loc[loc] = [0, 0]
    combined_df.sort_index(inplace=True)

    if plot_interpolation:
        fig, axs = plt.subplots(nrows=2, sharex=True)
        axs[0].plot(Ct_df.index, Ct_df.Ct, label="Original", color="k")
        axs[0].plot(
            combined_df.index, combined_df.Ct, label="Interpolated", ls="dotted"
        )
        axs[0].legend()
        axs[0].set_ylabel("Ct")

        axs[1].plot(
            RotSpeed_df.index, RotSpeed_df.RotSpeed, label="Original", color="k"
        )
        axs[1].plot(
            combined_df.index, combined_df.RotSpeed, label="Interpolated", ls="dotted"
        )
        axs[1].legend()
        axs[1].set_xlabel("Wind Speed")
        axs[1].set_ylabel("RotSpeed (rpm)")
        fig.suptitle("NREL 5MW Turbine")
        plt.savefig("ct_rotspeed.pdf", bbox_inches="tight")

    return combined_df


def write_turbine_yaml():
    ct_rotspeed_df = get_ct_rotspeed()
    yaml_data = {
        "JDM_5MW": {
            "Actuator_type": "JoukowskyDisk",
            "Actuator_rotor_diameter": 126,
            "Actuator_hub_height": 90,
            "Actuator_diameters_to_sample": 2.5,
            "Actuator_epsilon": [5.0, 5.0, 5.0],
            "Actuator_num_points_r": 40,
            "Actuator_num_points_t": 5,
            "Actuator_vortex_core_size": 24.0,
            "Actuator_use_tip_correction": True,
            "Actuator_use_root_correction": True,
            "Actuator_num_blades": 3,
            "Actuator_wind_speed": " ".join(
                [f"{v}" for v in list(ct_rotspeed_df.index)]
            ),
            "Actuator_rpm": " ".join([f"{v}" for v in list(ct_rotspeed_df.RotSpeed)]),
            "Actuator_thrust_coeff": " ".join(
                [f"{v}" for v in list(ct_rotspeed_df.Ct)]
            ),
        }
    }
    with open("test.yaml", "w") as yf:
        yaml = YAML(typ="safe")
        yaml.default_flow_style = False
        yaml.width = 1e6
        yaml.dump(yaml_data, yf)


if __name__ == "__main__":
    write_turbine_yaml()
