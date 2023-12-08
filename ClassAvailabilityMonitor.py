import requests

class ClassAvailabilityMonitor:
    def __init__(self, year, campus):
        self.year = year
        self.campus = campus
        self.classesDict = None

    def fetch_class_data(self):
        """
        Fetches class data from the API and stores it in the class dictionary.
        """
        api_url = f'https://sis.rutgers.edu/soc/api/openSections.json?year={self.year}&term=1&campus={self.campus}'
        with requests.Session() as s:
            response = s.get(api_url)
            rawData = response.text.strip('[]')
            formatted_data = rawData.split(',')
            self.classesDict = self.array_to_hash_table(formatted_data)

    @staticmethod
    def array_to_hash_table(array):
        """
        Converts an array into a hash table.
        """
        hash_table = {}
        for element in array:
            # Remove quotes and convert to integer
            key = int(element.strip('"'))
            hash_table[element.strip('"')] = key
        return hash_table

    def check_class_availability(self, index_of_class):
        """
        Checks if a class is available.
        """
        if self.classesDict is None:
            self.fetch_class_data()

        return index_of_class in self.classesDict
