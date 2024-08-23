from tourapi.AreaCodeAPI import AreaCodeAPI, Params


def generate_areacode_py():
    # There are many nested class (서울Code, 인천Code, ...)
    # There is only one class (AreaCode) that contains all nested classes

    with open("output", "w") as file:
        file.write("from utils.class_with_int import class_with_int\n\n")

        areacodeDefinition = "class AreaCode:\n"
        for item in AreaCodeAPI.get_items_all(
            Params(numOfRows=20, pageNo=1, areaCode=None)
        ):
            nested_name = f"{item.name}Code"
            areacodeDefinition += (
                f"    {item.name} = class_with_int({nested_name}, {item.code})\n"
            )

            nested_definition = f"class {nested_name}:\n"
            for nested_item in AreaCodeAPI.get_items_all(
                Params(numOfRows=20, pageNo=1, areaCode=int(item.code))
            ):
                nested_definition += f"    {nested_item.name} = {nested_item.code}\n"
            file.write(nested_definition)

        file.write(areacodeDefinition)


def main():
    # TODO: use temporary file to store the generated code
    # Then validate if current AreaCode.py is the same as the generated code
    try:
        generate_areacode_py()
    except Exception as e:
        print(e)
