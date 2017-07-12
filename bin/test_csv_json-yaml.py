#!/usr/bin/env python3

import addressbook

ab = addressbook.Addressbook()

cnt1 = addressbook.Contact('John', 'Doe')
cnt2 = addressbook.Contact('Jane', 'Doe')
cnt2.add_attr("email", "jane@doe.org")

ab += cnt1
ab += cnt2


csvfile = "./Data/FakeNameGenerator.csv"

ab += addressbook.from_csv(csvfile)


#outData = {ab.name:{}}
#outData[ab.name]['allowed attributes'] = ab.allowed_attrs_dict()
#outData[ab.name]['Contacts'] = ab.contacts_list()
#print(ab)
jsonout = csvfile.replace("csv","json")
addressbook.to_json(ab,jsonout)

yamlout = csvfile.replace("csv","yaml")
addressbook.to_yaml(ab,yamlout)

#with open(jsonout,"w") as jsonfile:
#    json.dump(outData,jsonfile,indent=4)

#    pass
#print(ab.full_print())

