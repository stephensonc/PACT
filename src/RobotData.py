class RobotData:

    def __init__(self, kg_weight, friction_coefficient, avg_movespeed, max_movespeed=0.0): 
        self.kg_weight = kg_weight
        self.friction_coefficient = friction_coefficient
        self.avg_movespeed = avg_movespeed
        self.max_movespeed = avg_movespeed if max_movespeed <= 0.0 else max_movespeed