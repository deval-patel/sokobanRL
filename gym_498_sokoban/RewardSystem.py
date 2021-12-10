class RewardSystem:
    @staticmethod
    def get_reward_for_move():
        """ for move without any effect """
        return -0.05

    @staticmethod
    def get_reward_for_box_on_target():
        return 8.0

    @staticmethod
    def get_reward_for_box_off_target():
        return -8.0

    @staticmethod
    def get_reward_for_invalid_move():
        return -3.0

    @staticmethod
    def get_reward_for_victory():
        return 30.0

    @staticmethod
    def get_reward_for_loss():
        return -30.0
