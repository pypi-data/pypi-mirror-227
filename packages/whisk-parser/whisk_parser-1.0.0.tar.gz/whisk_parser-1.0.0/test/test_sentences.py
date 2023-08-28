import unittest
import whisk_parser as wp


sentence_test_data = [
	(
		"""Car opportunity product according. Return well indicate.
		Improve point station throughout special leader show. Card according painting none she even perform per. But attack else mind she high score.
		my email is kristopher.fitzgeraldarroba garner.com
		Hand force strong. Ask key agreement write institution gun board. Gun describe short dark marriage common. Grow game edge.""",
		# ------
		"""
		Car opportunity product according. Return well indicate.
		Improve point station throughout special leader show. Card according painting none she even perform per. But attack else mind she high score.
		my email is kristopher.fitzgerald@garner.com
		Hand force strong. Ask key agreement write institution gun board. Gun describe short dark marriage common. Grow game edge.
		"""
	),
	(
		"""These pay prove. Small very article situation remember nation.
		Never career name writer house edge. Doctor character expert election small bill behind same. Democratic behind drive capital capital.
		envia un correo electronico a: christopher.gibsonarrobaconrad-flowers.com
		Wonder defense sometimes discussion involve year few. Structure western tough college news.""",
		# ------
		"""These pay prove. Small very article situation remember nation.
		Never career name writer house edge. Doctor character expert election small bill behind same. Democratic behind drive capital capital.
		envia un correo electronico a: christopher.gibson@conrad-flowers.com
		Wonder defense sometimes discussion involve year few. Structure western tough college news."""
	)
]

class TestWP(unittest.TestCase):
	def test_email_paragraph_parser(self):
		for datapoint in sentence_test_data:
			self.assertEqual(datapoint[1], wp.parse_email(datapoint[0]))