import unittest

from ediwheel.connector import *


class TestConnector(unittest.TestCase):

    def test_auth(self):
        michelin = EdiConnectorConfig( # nullpointer
            host="https://bibserve.com/MichelinSCEBE/AdhocA2XML25Servlet",
            username="MWH9337",
            password="AdHoc?ForiGrC931",
            id="6069966",
            timeout_s=10,
        )
        conti = EdiConnectorConfig( # Invalid credentials
            host="https://direct.conti.de/cgi-bin/easy-xml.cgi",
            username="07319622",
            password="Gr81st45Bg",
            id="07319622",
            timeout_s=10,
        )
        goodyear = EdiConnectorConfig( # NO BACKEND
            host="",
            username="50705723",
            password="GREFRO10032021",
            id="50705723",
            timeout_s=10,
        )
        vredestein = EdiConnectorConfig( # WORKS
            host="https://dealer.vredestein.com/adhocxml.dll",
            username="50705723",
            password="GREFRO10032021",
            id="50705723",
            timeout_s=10,
        )
        bridgestone = EdiConnectorConfig( # WORKS
            host="https://adhoc.bridgestone.eu/prod/adhoc",
            username="Bxp%A2",
            password="A2*Bxp",
            id="426009",
            timeout_s=10,
        )

        connector = EdiConnector(michelin)
        connector.enquiry("3528701696225", "169622")


