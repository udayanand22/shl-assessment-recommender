import pandas as pd
import re

class SHLScraper:
    def get_assessments(self):
        """Returns comprehensive assessment data"""
        return pd.DataFrame([
            {
                'name': 'Java Developer Test',
                'url': 'https://www.shl.com/java',
                'remote_testing': 'Yes',
                'adaptive_irt': 'No',
                'duration': '40 mins',
                'test_type': 'Coding'
            },
            {
                'name': 'JavaScript Assessment',
                'url': 'https://www.shl.com/javascript',
                'remote_testing': 'Yes',
                'adaptive_irt': 'No',
                'duration': '45 mins',
                'test_type': 'Coding'
            },
            {
                'name': 'Python & SQL Assessment',
                'url': 'https://www.shl.com/python-sql',
                'remote_testing': 'Yes',
                'adaptive_irt': 'No',
                'duration': '60 mins',
                'test_type': 'Technical'
            },
            {
                'name': 'Cognitive Ability Test',
                'url': 'https://www.shl.com/cognitive',
                'remote_testing': 'Yes',
                'adaptive_irt': 'Yes',
                'duration': '30 mins',
                'test_type': 'Psychometric'
            },
            {
                'name': 'Quick Screening Test',
                'url': 'https://www.shl.com/screening',
                'remote_testing': 'Yes',
                'adaptive_irt': 'No',
                'duration': '25 mins',
                'test_type': 'General'
            }
        ])
        