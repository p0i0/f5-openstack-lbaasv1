import netaddr
import os

OBJ_PREFIX = 'uuid_'


def prefixed(name):
    if not name.startswith(OBJ_PREFIX):
        name = OBJ_PREFIX + name
    return name


def icontrol_folder(method):
    """Decorator to put the right folder on iControl object."""
    def wrapper(*args, **kwargs):
        instance = args[0]
        if 'folder' in kwargs:
            kwargs['folder'] = os.path.basename(kwargs['folder'])
            if not kwargs['folder'] == 'Common':
                kwargs['folder'] = prefixed(kwargs['folder'])

            if 'name' in kwargs and kwargs['name']:
                if kwargs['name'].startswith('/Common/'):
                    kwargs['name'] = os.path.basename(kwargs['name'])
                    kwargs['name'] = prefixed(kwargs['name'])
                    kwargs['name'] = instance.bigip.set_folder(kwargs['name'],
                                                               'Common')
                else:
                    kwargs['name'] = os.path.basename(kwargs['name'])
                    kwargs['name'] = prefixed(kwargs['name'])
                    kwargs['name'] = instance.bigip.set_folder(kwargs['name'],
                                                           kwargs['folder'])

            if 'named_address' in kwargs and kwargs['named_address']:
                if kwargs['named_address'].startswith('/Common/'):
                    kwargs['named_address'] = \
                        os.path.basename(kwargs['named_address'])
                    kwargs['named_address'] = \
                        instance.bigip.set_folder(kwargs['named_address'],
                                                  'Common')
                else:
                    kwargs['named_address'] = \
                        os.path.basename(kwargs['named_address'])
                    kwargs['named_address'] = \
                        instance.bigip.set_folder(kwargs['named_address'],
                                                  kwargs['folder'])

            for name in kwargs:
                if name.find('_name') > 0 and kwargs[name]:
                    if kwargs[name].startswith('/Common/'):
                        kwargs[name] = os.path.basename(kwargs[name])
                        kwargs[name] = prefixed(kwargs[name])
                        kwargs[name] = instance.bigip.set_folder(kwargs[name],
                                                                 'Common')
                    else:
                        name_prefix = name[0:name.index('_name')]
                        specific_folder_name = name_prefix + "_folder"
                        folder = kwargs['folder']
                        if specific_folder_name in kwargs:
                            folder = kwargs[specific_folder_name]
                        kwargs[name] = os.path.basename(kwargs[name])
                        kwargs[name] = prefixed(kwargs[name])
                        kwargs[name] = instance.bigip.set_folder(kwargs[name],
                                                             folder)

            instance.bigip.set_folder(None, kwargs['folder'])

        return method(*args, **kwargs)
    return wrapper


def icontrol_rest_folder(method):
    """Decorator to put the right folder on iControl object."""
    def wrapper(*args, **kwargs):
        if 'folder' in kwargs:
            if kwargs['folder'].find('Common') < 0:
                kwargs['folder'] = \
                    kwargs['folder'].replace('~', '').replace('/', '')
                if not kwargs['folder'].startswith(OBJ_PREFIX):
                    kwargs['folder'] = OBJ_PREFIX + kwargs['folder']
        if 'name' in kwargs and kwargs['name']:
            if kwargs['name'].find('/') > -1:
                kwargs['name'] = os.path.basename(kwargs['name'])
            if kwargs['name'].find('~') > -1:
                path_parts = kwargs['name'].split('~')
                kwargs['name'] = path_parts[-1]
            if not kwargs['name'].startswith(OBJ_PREFIX):
                kwargs['name'] = OBJ_PREFIX + kwargs['name']
        for name in kwargs:
            if name.find('_name') > 0 and kwargs[name]:
                if kwargs[name].find('/') > -1:
                    kwargs[name] = os.path.basename(kwargs[name])
                if kwargs[name].find('~') > -1:
                    path_parts = kwargs[name].split('~')
                    kwargs[name] = path_parts[-1]
                if not kwargs[name].startswith(OBJ_PREFIX):
                    kwargs[name] = OBJ_PREFIX + kwargs[name]
        return method(*args, **kwargs)
    return wrapper


def domain_address(method):
    """Decorator to put the right route domain decoration an address."""
    def wrapper(*args, **kwargs):
        instance = args[0]
        if not instance.bigip.route_domain_required:
            return method(*args, **kwargs)

        folder = 'Common'
        if 'folder' in kwargs:
            folder = os.path.basename(kwargs['folder'])
            if not folder == 'Common':
                if not folder.startswith(OBJ_PREFIX):
                    folder = OBJ_PREFIX + folder
        for name in kwargs:
            if name.find('mask') > -1:
                if isinstance(kwargs[name], list):
                    for mask in kwargs[name]:
                        netaddr.IPAddress(mask)
                else:
                    if kwargs[name]:
                        netaddr.IPAddress(kwargs[name])
            if name.find('ip_address') > -1:
                if kwargs[name]:
                    if name.find('_ip_address') > -1:
                        name_prefix = name[0:name.index('_ip_address')]
                        specific_folder_name = name_prefix + "_folder"
                        if specific_folder_name in kwargs:
                            folder = kwargs[specific_folder_name]
                    if instance.bigip.route_domain_required:
                        if isinstance(kwargs[name], list):
                            return_list = []
                            for address in kwargs[name]:
                                decorator_index = address.find('%')
                                if decorator_index < 0:
                                    netaddr.IPAddress(address)
                                    rid = instance.bigip.get_domain_index(
                                                                     folder)
                                    if rid > 0:
                                        address = address + "%" + str(rid)
                                else:
                                    netaddr.IPAddress(
                                                   address[:decorator_index])
                                return_list.append(address)
                            kwargs[name] = return_list
                        else:
                            decorator_index = kwargs[name].find('%')
                            if decorator_index < 0:
                                netaddr.IPAddress(kwargs[name])
                                rid = instance.bigip.get_domain_index(folder)
                                if rid > 0:
                                    kwargs[name] = kwargs[name] + \
                                                            "%" + str(rid)
                            else:
                                netaddr.IPAddress(
                                               kwargs[name][:decorator_index])
                    else:
                        if isinstance(kwargs[name], list):
                            for address in kwargs[name]:
                                netaddr.IPAddress(address)
                        else:
                            netaddr.IPAddress(kwargs[name])
        return method(*args, **kwargs)
    return wrapper


def decorate_name(name=None, folder='Common'):
    folder = os.path.basename(folder)
    if not folder == 'Common':
        if not folder.startswith(OBJ_PREFIX):
            folder = OBJ_PREFIX + folder

    if name.startswith('/Common/'):
        name = os.path.basename(name)
        if not name.startswith(OBJ_PREFIX):
            name = OBJ_PREFIX + name
        name = '/Common/' + name
    else:
        name = os.path.basename(name)
        if not name.startswith(OBJ_PREFIX):
            name = OBJ_PREFIX + name
        name = '/' + folder + '/' + name
    return name


def strip_folder_and_prefix(path):
    if isinstance(path, list):
        for i in range(len(path)):
            if path[i].startswith('/Common'):
                path[i] = path[i].replace(OBJ_PREFIX, '')
            else:
                path[i] = \
                  os.path.basename(str(path[i])).replace(OBJ_PREFIX, '')
        return path
    else:
        if path.startswith('/Common'):
            return str(path).replace(OBJ_PREFIX, '')
        else:
            return os.path.basename(str(path)).replace(OBJ_PREFIX, '')
