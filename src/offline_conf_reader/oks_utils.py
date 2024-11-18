

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


def get_many(root, start_obj, object_name=None, class_name=None):
    ret = []
    if object_name is None and class_name is None:
        raise ValueError('Either \'object_name\' or \'class_name\' must be provided')

    for child in start_obj:
        this_class_name = child.attrib.get('class')
        if (class_name is not None) and (this_class_name is not None) and (this_class_name != class_name):
            continue

        this_object_name = child.attrib.get('name')
        if child.tag == 'obj' and this_object_name is None:
            this_object_name = child.attrib.get('id')

        if (object_name is not None) and (this_object_name is not None) and (this_object_name != object_name):
            continue

        print(f'object {this_object_name} satisfies name {object_name} and class {class_name}')

        if child.tag in ['attr', 'obj']:
            ret += [child]

        if child.tag == 'rel':
            for obj in root.findall('obj'):
                if obj.attrib['id'] != child.attrib['id']:
                    continue
                ret += [obj]

    return ret


def get_one(root, start_obj, object_name=None, class_name=None):
    ret = get_many(root, start_obj, object_name, class_name)
    if ret == []:
        raise ValueError(f'Could not find object with name \'{object_name}\' or class \'{class_name}\' in {start_obj.attrib["id"]}, which is composed of: {[s.attrib["name"] for s in start_obj]}')
    elif len(ret) > 1:
        raise ValueError(f'Too many object satify name \'{object_name}\' or class \'{class_name}\' in {start_obj.attrib["id"]}, which is composed of: {[s.attrib["name"] for s in start_obj]}')

    return ret[0]


def find_session(root, session_name):
    return get_one(root, root, class_name='Session', object_name=session_name)
