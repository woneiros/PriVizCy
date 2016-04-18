
##  GET WEB CLASSIFICATION - PriVizCy
#    WillahScott - April, 2016
#
#  Obtains the classification of a given list of URLs from fortiguard.com
#

from selenium import webdriver


class WebClassifier(object):
	''' Simple crawler to classify webpages using fortiguard.com web '''
	QUERY = "http://fortiguard.com/iprep?data={domain}&lookup=Lookup"

	def __init__(self, invisible=True):
		# Initializes the webdriver
		if invisible:
			self.driver = webdriver.PhantomJS()
		else:
			self.driver = webdriver.Firefox()


	def get_classification(self, target):
		''' Classifies a given url (or set of urls) using the service: fortiguard.com '''	

		self.driver.get( self.QUERY.format(domain=target) )  # query fortiguard.com

		# Locate the classification
		_content = self.driver.find_element_by_id("content_wrapper")
		raw = _content.find_element_by_tag_name("h3").text

		# Parse and return
		category = raw.split(':')[1].strip()
		return category


	def get_classifications(self, target_list, verbose=False):
		''' Classifies a given set of urls using the service: fortiguard.com '''

		results = []
		count = 0  # initialize counter

		if verbose:
			total = len(target_list)
			print('\nClassifying {} URLs. Fetching ...'.format(total))
			print('   - PROGRESS: ', end='')

			step = total // 10  # step update

		for target in target_list:
			_classif = self.get_classification(target)
			results.append(_classif)

			count += 1
			if verbose and count % step == 0:
				print ('##', end='')

		print('  DONE')
		return results


	def close(self):
		''' Close the webdriver '''
		self.driver.close()
		
