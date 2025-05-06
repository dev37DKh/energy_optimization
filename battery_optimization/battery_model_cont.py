class ContinuousBattery:
    """
    A continuous‐time battery model:
      dE/dt = η_c * P_charge  -  P_discharge / η_d
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
    ):
        assert 0 <= soc_init <= 1
        assert 0 <= soc_min < soc_max <= 1
        self.capacity = capacity_kwh
        self.E = soc_init * capacity_kwh
        self.soc_min = soc_min * capacity_kwh
        self.soc_max = soc_max * capacity_kwh
        self.eta_c = eta_c
        self.eta_d = eta_d

    @property
    def soc(self) -> float:
        """Current state‐of‐charge [0..1]."""
        return self.E / self.capacity

    def dE_dt(self, p_grid: float) -> float:
        """
        Differential change of stored energy [kW]:
          p_grid>0 → charge, <0 → discharge
        """
        if p_grid >= 0:
            return p_grid * self.eta_c
        else:
            return p_grid / self.eta_d

    def clamp(self):
        """Enforce E ∈ [soc_min, soc_max]."""
        self.E = max(self.soc_min, min(self.E, self.soc_max))

    def integrate_euler(self, p_profile, t_profile):
        """
        Simple Euler integration over a time series.
        Args:
          p_profile: list or array of p_grid values [kW]
          t_profile: list or array of timestamps [h], same length
        Returns:
          soc_trajectory: list of soc at each timestamp
        """
        soc_trajectory = []
        for i in range(1, len(t_profile)):
            dt = t_profile[i] - t_profile[i-1]
            dE = self.dE_dt(p_profile[i-1]) * dt
            self.E += dE
            self.clamp()
            soc_trajectory.append(self.soc)
        return soc_trajectory