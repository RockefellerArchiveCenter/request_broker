from asnake.aspace import ASpace
from request_broker import settings


class Routine:
    """
    Base routine class which is inherited by all other routines.

    Provides default clients for ArchivesSpace.
    """

    def __init__(self):
        self.aspace = ASpace(baseurl=settings.ARCHIVESSPACE["baseurl"],
                             username=settings.ARCHIVESSPACE["username"],
                             password=settings.ARCHIVESSPACE["password"],
                             repository=settings.ARCHIVESSPACE["repo_id"])


class ProcessRequest(Routine):
    # TODO: main section where processing happens
    # Push requests to submitted or unsubmitted
    # If open and delivery formats, mark as submittable
    # TO DO: add code to read through the rights in order
    # 1. PREMIS rights statements first
    # 2. Conditions governing access notes
    # 3. Next closest conditions governing access notes/rights statements (inherited)
    """
    Runs through the process of iterating through requests, getting json information,
    checking delivery formats, checking restrictrions, and adding items to lists.
    """

    def get_data(self, item):
        """Gets an archival object from ArchivesSpace.

        Args:
            item (str): An ArchivesSpace URI.

        Returns:
            obj: An ArchivesSpace Archival Object.
        """
        obj = self.aspace.client.get(item)
        if obj.status_code == 200:
            return obj.json()
        else:
            raise Exception(obj.json()["error"])

    def inherit_restrictions(obj):
        """Iterates up from an archial object level to find the nearest restriction
        act or restriction note.

        Args:
            obj: An ArchivesSpace archival object.
        """
        # TODO: Add code to look up and inherit accessrestrict notes. Will need
        # to address resource records at some point.
        pass

    def check_formats(obj):
        """Parses instances and creates a list of instance types. Matches list against
        list of acceptable delivery formats. Acceptable formats include digital,
        microform, or mixed materials.

        Args:
            obj (JSONModelObject): an ArchivesSpace archival object.

        Returns:
            bool: True on any match with delivery formats. None on no match or instances.
        """
        formats = []
        if obj.instances:
            for instance in obj.instances:
                if instance.instance_type in formats:
                    return True
                else:
                    return None
        else:
            return None

    def return_formats(obj):
        # TO DO: Expand to log if digital objects exist so we can log whether to send duplication or retreival requests.
        """Returns a list of acceptable delivery formats for an archival object.

        Args:
            obj: An ArchivesSpace archival object.

        Returns:
            list: list of instance objects that match delivery formats.
        """
        for instance in obj.instances:
            pass

    def process_email_request(self, object_list):
        """Processes email requests.

        Args:
            object_list (list): A list of AS archival object URIs.

        Returns:
            data (list): A list of dicts of objects.
        """
        for item in object_list:
            try:
                self.get_data(item)
                print('after get_data')
            except Exception as e:
                print(e)
            return 'test'

    def process_readingroom_request(self, object_list):
        """Processes reading room requests.

        Args:
            object_list (list): A list of AS archival object URIs.

        Returns:
            submitted (list): A list of dicts of submittable objects with corresponding most
                desirable delivery format.
            unsubmitted (list): A list of dicts of unsubmittable objects with corresponding
                reason of failure.
        """
        for item in object_list:
            try:
                data = self.get_data(item)
            except Exception as e:
                print(e)
            return 'test'

    def process_duplication_request(self, object_list):
        """Processes duplication requests.

        Args:
            object_list (list): A list of AS archival object URIs.

        Returns:
            submitted (list): A list of dicts of submittable objects with corresponding most
                desirable delivery format.
            unsubmitted (list): A list of dicts of unsubmittable objects with corresponding
                reason of failure.
        """
        for item in object_list:
            try:
                self.get_data(item)
                print('after get_data')
            except Exception as e:
                print(e)
            return 'test'

    def process_csv_request(self, object_list):
        """Processes requests for a CSV download.

        Args:
            object_list (list): A list of AS archival object URIs.

        Returns:
            A streaming CSV file
        """
        for item in object_list:
            try:
                self.get_data(item)
                print('after get_data')
            except Exception as e:
                print(e)
            return 'test'


class DeliverEmail(Routine):
    """Sends an email with request data to an email address or list of addresses.
    """
    pass


class DeliverReadingRoomRequest(Routine):
    """Sends submitted data to Aeon for transaction creation in Aeon.
    """
    pass


class DeliverDuplicationRequest(Routine):
    """Sends submitted data for duplication request creation in Aeon.
    """


class DeliverCSV(Routine):
    """Create a streaming csv file based on original request.
    """
    pass
