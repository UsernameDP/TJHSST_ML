import sys
import csv

# Goal is to find data that is injective to a given attribute

args = sys.argv[1:]

file_path = args[0]


def checkAttribute():
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        first_row = next(reader)

        attributes = list(first_row)

        for indx, attribute in enumerate(attributes):
            print(f"{indx} : {attribute}")

        attribute_to_check_indx = int(
            input("Which Attribute do you want to check [INDEX] : ")
        )
        attribute_to_check = attributes[attribute_to_check_indx]
        print(f"Checking : {attribute_to_check}")

        attribute_valuesDict_list = [{} for _ in range(len(attributes))]
        attributesIndx_to_check_set = set([i for i in range(len(attributes))])
        attributesIndx_to_check_set.remove(attribute_to_check_indx)

        for i, row in enumerate(reader):
            # if i == 10000:  # stop after 3 rows
            #     break

            if len(attributesIndx_to_check_set) == 0:
                break

            attribute_to_check_val = row[attribute_to_check]

            attributes_to_remove = []

            for attribute_indx in attributesIndx_to_check_set:
                row_attribute_val = row[attributes[attribute_indx]]
                attribute_dict = attribute_valuesDict_list[attribute_indx]

                if row_attribute_val not in attribute_dict:
                    attribute_dict[row_attribute_val] = attribute_to_check_val
                    continue

                if attribute_dict[row_attribute_val] != attribute_to_check_val:
                    # implies not injective
                    attributes_to_remove.append(attribute_indx)

            for attribute_indx in attributes_to_remove:
                attributesIndx_to_check_set.remove(attribute_indx)

        print(attributesIndx_to_check_set)

        for attribute_indx in attributesIndx_to_check_set:
            print(f"{attribute_indx} ({attributes[attribute_indx]})")
            for k, v in list(attribute_valuesDict_list[attribute_indx].items())[:10]:
                print(k, v)
            print()


def checkAllAttributes():

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        first_row = next(reader)

        attributes = list(first_row)

        for i in range(len(attributes)):
            attribute_to_check_indx = i
            attribute_to_check = attributes[attribute_to_check_indx]
            print(f"Checking : {attribute_to_check}")

            attribute_valuesDict_list = [
                {} for _ in range(len(attributes))
            ]  # key represents {OTHERvalue : CHECKvalue}
            attributesIndx_to_check_set = set([i for i in range(len(attributes))])
            attributesIndx_to_check_set.remove(attribute_to_check_indx)

            f.seek(0)
            reader = csv.DictReader(f)
            next(reader)
            for i, row in enumerate(reader):

                if len(attributesIndx_to_check_set) == 0:
                    break

                attribute_to_check_val = row[attribute_to_check]

                attributes_to_remove = []

                for attribute_indx in attributesIndx_to_check_set:
                    row_attribute_val = row[
                        attributes[attribute_indx]
                    ]  # value of OTHER attribute
                    attribute_dict = attribute_valuesDict_list[
                        attribute_indx
                    ]  # dictionary

                    if row_attribute_val not in attribute_dict:
                        attribute_dict[row_attribute_val] = attribute_to_check_val
                        continue

                    if attribute_dict[row_attribute_val] != attribute_to_check_val:
                        # implies not injective
                        attributes_to_remove.append(attribute_indx)

                for attribute_indx in attributes_to_remove:
                    attributesIndx_to_check_set.remove(attribute_indx)

            attributesIndx_to_check_list = list(attributesIndx_to_check_set)
            attributesIndx_to_check_list.sort()

            print(
                f"{attribute_to_check_indx} ({attributes[attribute_to_check_indx]}) : {attributesIndx_to_check_list} -> { [ attributes[i] for i in attributesIndx_to_check_list ] }"
            )


checkAllAttributes()
checkAttribute()
