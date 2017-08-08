"""
Here I will compose some settings and paths based on args and aettings I can obtain or found.

"""
# from check.parse_args import ArgsParse


class LocalLogic:

    def __init__(self, logging, parsable_args_set, operational_args, addm_args_set):

        self.logging = logging
        self.parsable_args_set = parsable_args_set
        self.operational_args = operational_args
        self.addm_args_set = addm_args_set

    def tkn_tree(self):
        """
        Compose paths to usual TKN tree dirs

        :return:
        """
        log = self.logging
        print(self.parsable_args_set)
        if self.parsable_args_set['file_ext'] == 'tplpre':
            log.debug("Dev pattern")
