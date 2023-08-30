import os
import unittest

from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from pydriller import Git

from reposcorer.attributes.iac import iac_ratio


ROOT = os.path.realpath(__file__).rsplit(os.sep, 3)[0]
PATH_TO_REPO = str(Path(os.path.join(ROOT, 'test_data', 'terraform-aws-ec2')))


class AttributesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.git_repo = Git(PATH_TO_REPO)
        cls.git_repo.reset()

    @classmethod
    def tearDownClass(cls):
        cls.git_repo.reset()

    @staticmethod
    def test_terraform_iac_ratio():
        assert round(iac_ratio(PATH_TO_REPO), 2) == 0.5714




if __name__ == '__main__':
    unittest.main()
