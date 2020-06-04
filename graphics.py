class Graphics:
    START_X = 50
    START_Y = 50

    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None

    TROLLEY_X_INIT = 50
    TROLLEY_Y_INIT = None

    #   -----------------------------------------

    load = None
    trolley = None
    massless_cable = None

    #   -----------------------------------------

    response_x = 0.0

    cable_distance = 3.0

    trolley_x = 0.0
    load_x = 0.0
    load_y = 0.0

    delta_t = 0.02

    def __init__(self, screenWidth, screenHeight):
        #   SCREEN PARAMS
        self.SCREEN_WIDTH = screenWidth
        self.SCREEN_HEIGHT = screenHeight
        self.TROLLEY_Y_INIT = screenWidth - 800

        #   CABLE
        self.massless_cable = MassLessCable(self.cable_distance)

        #   TROLLEY
        self.trolley = Trolley(self.SCREEN_HEIGHT, self.TROLLEY_X_INIT, self.delta_t)

        #   MASS LOAD
        self.load = Load(self.cable_distance)

    def RefreshGraphics(self, output):
        #   Main scenario
        Scenario.Draw(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)

        #   Trolley
        self.trolley.Draw()
        self.trolley_x = self.trolley.Get_X_Position();

        #   Load
        self.load_x, self.load_y = self.load.Draw(self.trolley_x, output)

        #   MassLess Cable
        self.massless_cable.Draw(self.trolley.x, self.load_x, self.load_y)

        return self.trolley_x