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
    import io, sys
    from xml.etree.ElementTree import ElementTree
    stream = io.BytesIO()
    element = dict_to_xml('organisation', thing)
    ElementTree(element).write(stream, encoding='utf-8', xml_declaration=True)
    return stream.getvalue().lstrip()


def to_csv(thing):
    import csv, io
    fieldnames = list(thing.keys())
    row = thing.values()
    stream = io.StringIO()
    writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames,
            delimiter=',',
            lineterminator='\r\n',
            quotechar='"',
            quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerow(thing)
    text = stream.getvalue().lstrip()
    return text
