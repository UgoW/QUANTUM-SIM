class WavePacket(WaveFunction):
    def __init__(self, momentum_distribution=None, plane_waves=None, 
                 position_center: float = 0.0, time: float = 0.0):
        if plane_waves is not None:
            self.plane_waves = plane_waves
            self.momentum_distribution = self._distribution_from_waves()
        elif momentum_distribution is not None:
            self.momentum_distribution = momentum_distribution
            self.plane_waves = []
        else:
            raise ValueError("Either momentum_distribution or plane_waves must be provided")
        
        self.position_center = position_center
        super().__init__(np.array([position_center]), time)
    
    def _distribution_from_waves(self) -> Callable:
        def dist(k: float) -> complex:
            return sum(pw.amplitude for pw in self.plane_waves 
                      if abs(pw.wave_number - k) < 1e-10)
        return dist