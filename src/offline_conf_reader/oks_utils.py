

class OKSValueError(Exception):
    pass


def get_many_object(root, object_id=None, class_name=None):
    ret = []

    should_check_id = object_id is not None
    should_check_class = class_name is not None

    for child in root:
        if child.tag != 'obj':
            continue

        if should_check_id and child.attrib['id'] != object_id:
            continue

        if should_check_class and child.attrib['class'] != class_name:
            continue

        ret += [child]

    if ret == []:
        raise OKSValueError(f'Expected to find at least one object ({object_id=}, {class_name=}), but found none')

    return ret


def get_one_object(root, object_id=None, class_name=None):
    ret = get_many_object(root, object_id, class_name)

    if len(ret) != 1:
        raise OKSValueError(f'Expected to find exactly one object ({object_id=}, {class_name=}), but found {len(ret)}')

    return ret[0]


def get_many_relation_by_class(root, start_object, name=None):
    ret = []

    for child in start_object:
        if child.tag != 'rel':
            continue

        for grand_child in child:

            ret += [
                get_one_object(
                    root,
                    object_id = grand_child.attrib['id'],
                    class_name = name,
                )
            ]

    return ret


def get_many_relation_by_name(root, start_object, name=None):
    ret = []

    for child in start_object:
        if child.tag != 'rel':
            continue

        if child.attrib['name'] != name:
            continue

        for grand_child in child:
            ret += [
                get_one_object(
                    root,
                    object_id = grand_child.attrib['id'],
                    class_name = grand_child.attrib['class'],
                )
            ]

    if ret == []:
        raise OKSValueError(f'Expected to find at least one relation ({name=}), but found none')
    return ret


def get_one_relation_by_class(root, start, name=None):
    ret = []

    for child in start:
        if child.tag != 'rel':
            continue

        if child.attrib['class'] != name:
            continue

        ret += [
            get_one_object(
                root,
                object_id = child.attrib['id'],
                class_name = name,
            )
        ]
    if len(ret) != 1:
        raise OKSValueError(f'Expected to find exactly one relation (class {name}), but found {len(ret)}')

    return ret[0]


def get_one_relation_by_name(root, start, name=None, catch_oks_value_errors=False):
    ret = []

    for child in start:
        if child.tag != 'rel':
            continue

        if child.attrib['name'] != name:
            continue

        try:
            obj = get_one_object(
                root,
                object_id = child.attrib['id'],
                class_name = child.attrib['class'],
            )
            ret += [obj]
        except OKSValueError as e:
            if catch_oks_value_errors:
                continue
            raise e

    if len(ret) != 1:
        raise OKSValueError(f'Expected to find exactly one relation (class {name}), but found {len(ret)}')

    return ret[0]


def get_one_attribute(root, start_object, name=None):
    ret = []

    for child in start_object:
        if child.tag != 'attr':
            continue

        if child.attrib['name'] != name:
            continue

        ret += [child]

    if len(ret) != 1:
        raise OKSValueError(f'Expected to find exactly one attribute ({name=}), but found {len(ret)}')

    return ret[0]


def find_session(root, session_name):

    return get_one_object(
        root = root,
        class_name = 'Session',
        object_id = session_name
    )


def get(root, start_object, name):
    try:
        return get_many_relation_by_name(root, start_object, name)
    except OKSValueError:
        pass

    try:
        return get_one_relation_by_name(root, start_object, name, catch_oks_value_errors=True)
    except OKSValueError:
        pass

    return get_one_attribute(root, start_object, name)



def check_for_data_includes(root):

    for child in root:
        if child.tag != 'include':
            continue
        for include_file in child:
            if include_file.tag != 'file':
                continue
            if include_file.attrib['path'].endswith('.schema.xml'):
                continue
            return True

    return False

def oks_cast(value, type_name):
    # Unsupported: date, time, uid, enum, class

    if type_name in ['s8', 'u8', 's16', 'u16', 's32', 'u32', 's64', 'u64']:
        return int(value)
    elif type_name in ['float', 'double']:
        return float(value)
    elif type_name == 'bool':
        return bool(int(value))

    print(f'Unsupported type {type_name} for value {value}, returning a string')
    return str(value)


def get_value(attribute):
    return oks_cast(attribute.attrib['val'], attribute.attrib['type'])
