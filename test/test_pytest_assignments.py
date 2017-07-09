import addressbook
import pytest

def test_add_Contact_to_Addressboek():
    addressbk = addressbook.Addressbook()
    contact = addressbook.Contact("John", "Doe")
    prelength = len(addressbk)
    addressbk.add_contact(contact)
    postlength = len(addressbk)

    assert postlength - prelength == int(1)

def test_non_Contact_cannot_be_added_to_addressbook():    
    addressbk = addressbook.Addressbook()
    non_contact ="John Doe"
    with pytest.raises(TypeError):
        addressbk.add_contact(non_contact)

def test_Addressbook_can_be_searched_for_Contact_with_Name():
    addressbk = addressbook.Addressbook()
    c1 = addressbook.Contact("John", "Doe")
    c2 = addressbook.Contact("Jane", "Doe")
    c3 = addressbook.Contact("Pietje", "Puk")

    addressbk.add_contact(c1)
    addressbk.add_contact(c2)
    addressbk.add_contact(c3)
    
    foundC = addressbk.find_contact_by_name("Pietje","Puk")
    firstFind = foundC[0]
    assert firstFind == c3 
