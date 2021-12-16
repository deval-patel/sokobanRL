class RewardSystem:
    @staticmethod
    def get_reward_for_move():
        """ for move without any effect """
        return -0.05

    @staticmethod
    def get_reward_for_box_on_target():
        """ for moving a box onto a target """
        return 8.0

    @staticmethod
    def get_reward_for_box_off_target():
        """ for moving a box off the target """
        return -8.0

    @staticmethod
    def get_reward_for_invalid_move():
        """ for taking an action which results in an invalid move """
        return -3.0

    @staticmethod
    def get_reward_for_victory():
        """ for winning the level """
        return 30.0

    @staticmethod
    def get_reward_for_loss():
        """ for losing the level """
        return -30.0
