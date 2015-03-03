def log_traceback(logger, ex, ex_traceback=None):
    import traceback
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [ line.rstrip('\n') for line in
                 traceback.format_exception(ex.__class__, ex, ex_traceback)]
    logger.info(tb_lines)


def dict_to_xml(tag, thing):
    from xml.etree.ElementTree import Element
    elem = Element(tag)
    for key, val in thing.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem


def to_xml(thing):
    # TODO - crazily the tostring method can't be make to include xml
    # declaration. find another way
    from xml.etree.ElementTree import tostring
    element = dict_to_xml('organisation', thing)
    return tostring(element, 'utf-8')
