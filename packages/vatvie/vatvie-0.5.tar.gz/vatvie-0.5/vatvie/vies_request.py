
import requests as requests
import xml.etree.ElementTree as ET


class VatRequest:
    def __init__(self, country_code, vat_number):
        self.country_code = country_code 
        self.vat_number = vat_number 
        self._API_ENDPOINT = 'http://ec.europa.eu/taxation_customs/vies/services/checkVatTestService.wsdl'
    
    def get_api_soap(self):
        body = f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
                <soapenv:Header/>
                <soapenv:Body>
                    <urn:checkVat>
                        <urn:countryCode>{self.country_code}</urn:countryCode>
                        <urn:vatNumber>{self.vat_number}</urn:vatNumber>
                    </urn:checkVat>
                </soapenv:Body>
                </soapenv:Envelope>
                """
        
        response = requests.post(url = self._API_ENDPOINT, data = body)
        root = ET.fromstring(response.text)

        response_dict = {}


        for child in root.find(".//ns2:checkVatResponse", namespaces={"ns2": "urn:ec.europa.eu:taxud:vies:services:checkVat:types"}):
            tag = child.tag.split("}")[1]  
            text = child.text.strip() if child.text else ""
            response_dict[tag] = text
        
        return response_dict
    