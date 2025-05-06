class DiscreteBattery:
    """
    A simple discrete‐time battery:
      E_{t+1} = E_t + Δt * (η_c * P_charge_t - P_discharge_t / η_d)
      soc = E / capacity
    """

    def __init__(
        self,
        capacity_kwh: float,
        soc_init: float = 0.5,
        soc_min: float = 0.0,
        soc_max: float = 1.0,
        eta_c: float = 0.95,
        eta_d: float = 0.95,
        p_charge_max: float = None,
        p_discharge_max: float = None,
    ):
        assert 0 <= soc_init <= 1
        assert 0 <= soc_min < soc_max <= 1
        self.capacity = capacity_kwh
        self.soc = soc_init
        self.soc_min = soc_min
        self.soc_max = soc_max
        self.eta_c = eta_c
        self.eta_d = eta_d
        self.p_charge_max = p_charge_max or float("inf")
        self.p_discharge_max = p_discharge_max or float("inf")

    @property
    def energy(self) -> float:
        """Stored energy [kWh]."""
        return self.soc * self.capacity

    def step(self, p_grid: float, dt_h: float):
        """
        Advance the model by dt_h hours with grid power p_grid [kW]:
          p_grid > 0 → charging, < 0 → discharging
        """
        if p_grid >= 0:
            p_in  = min(p_grid, self.p_charge_max)
            e_in  = p_in * dt_h * self.eta_c
            delta =  e_in / self.capacity
        else:
            p_out = min(-p_grid, self.p_discharge_max)
            e_out = p_out * dt_h / self.eta_d
            delta = -e_out / self.capacity

        # update and clamp soc
        self.soc = max(self.soc_min, min(self.soc + delta, self.soc_max))


