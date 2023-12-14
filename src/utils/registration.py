from abc import ABC
from BO.datatypes import *
from BO.enums import *
from datetime import date
from utils.librarycard import LibraryCard
from utils.barcodeReader import BarcodeReader
import uuid


class AccountRegistrationManager:
    @staticmethod
    def register_new_member(registration_info: RegistrationInfo):
        card_number: LibraryCard = LibraryCard.genrate_card_number()
        bar_code: BarcodeReader = BarcodeReader.barcode_genrator()
        new_id: uuid.UUID = uuid.uuid4()
        password: uuid.UUID = uuid.uuid4()
        library_card: LibraryCard = LibraryCard(card_number, bar_code, date.today())
        address: Address = Address(
            registration_info.street_address,
            registration_info.city,
            registration_info.state,
            registration_info.zipcode,
            registration_info.country,
        )
        person: Person = Person(
            registration_info.name,
            address,
            registration_info.email,
            registration_info.phone,
        )

        return (new_id, password, person, date.today(), library_card)
