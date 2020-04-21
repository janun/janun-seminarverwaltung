from tablib import Dataset
from django.test import TestCase
from backend.seminars.resources import SeminarResource


class SeminarsImportTestCase(TestCase):
    def test_invalid_status(self):
        """test that a csv line with invalid status is rejected"""

        csv = """id,title,status,start_date,end_date
        5,Test-Seminarasd,asdasdad,2020-05-01,2020-05-01"""

        resource = SeminarResource()
        dataset = Dataset()
        dataset.load(csv, format="csv")
        result = resource.import_data(
            dataset, dry_run=True, raise_errors=False, use_transactions=True
        )
        self.assertTrue(result.has_validation_errors())

    def test_invalid_owner(self):
        """test that a csv line with an invalid owner is rejected"""

        csv = """title,start_date,end_date,owner
        Test-Seminar,2020-05-01,2020-05-01,asdasda"""

        resource = SeminarResource()
        dataset = Dataset()
        dataset.load(csv, format="csv")
        result = resource.import_data(
            dataset, dry_run=True, raise_errors=False, use_transactions=True
        )
        self.assertTrue(result.has_errors())
