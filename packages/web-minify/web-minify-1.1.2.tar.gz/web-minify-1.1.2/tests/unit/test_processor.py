import logging
import web_minify.processor
import web_minify.handlers.html.webparser

import datetime
import pprint
import time
import os
import html
import copy
import gc


logger = logging.getLogger(__name__)

do_debug = False


start_time = 1634600000  # datetime.datetime.now().timestamp()


def go_into_test_dir(test_dir="test_dir"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_test_dir = os.path.join(current_dir, test_dir)
    if not os.path.exists(abs_test_dir):
        os.mkdir(abs_test_dir)
    logger.info(f"CUR DIR {current_dir}.")
    logger.info(f"TEST DIR REL {test_dir}.")
    logger.info(f"TEST DIR ABS {abs_test_dir}.")
    logger.info(f"CWD BEFORE {os.getcwd()}.")
    os.chdir(abs_test_dir)
    logger.info(f"CWD AFTER  {os.getcwd()}.")


def get_mtime(filename):
    return os.path.getmtime(filename)


def set_mtime(filename, t):
    os.utime(filename, (t, t))


def create_dummy_file(filename, content, time=None):
    with open(filename, "w", encoding="utf-8") as file:
        written = file.write(content)
        assert written == len(content)
    if time:
        set_mtime(filename, time)
    actual_time = get_mtime(filename)
    if do_debug:
        logger.info(f"Created dummy file '{filename}' with {len(content)} bytes and mtime {time} (actual {actual_time})")
    return actual_time


def rm_if_exists(filename, do_debug=False):
    if filename and os.path.exists(filename):
        if do_debug:
            logger.info(f"Removed existing file '{filename}'")
        os.remove(filename)
    else:
        if do_debug:
            logger.info(f"File '{filename}' not removed (did not exist)")


def create_file_combo(label, base_filename, a_content, b_content, base_time, a_exists, b_exists, a_is_b, b_time_delta_s):
    a_filename = base_filename
    b_filename = a_filename
    b_content = a_content
    a_empty = not a_content or len(a_content) < 0
    b_empty = not b_content or len(b_content) < 0
    a_time = base_time
    b_time = a_time
    if a_is_b:
        # Handle case where files are the same
        # Start with no files
        rm_if_exists(a_filename)
        # Create files as needed
        if a_exists:
            create_dummy_file(a_filename, a_content, a_time)
    else:
        a_filename = "a." + base_filename
        b_filename = "b." + base_filename
        a_time = base_time
        b_time = base_time + b_time_delta_s
        # Start with no files
        rm_if_exists(a_filename)
        rm_if_exists(b_filename)
        # Create files as needed
        if a_exists:
            if a_exists:
                create_dummy_file(a_filename, a_content, a_time)
        if b_exists and not a_is_b:
            if b_exists:
                create_dummy_file(b_filename, b_content, b_time)

    # fmt:off
    ret={
          "label": label 
        , "base_filename": base_filename
        , "base_time": base_time
        , "a":{
              "exists": a_exists
            , "empty": a_empty
            , "filename": a_filename
            , "content": a_content
            , "size": len(a_content)
            , "time": a_time
            , "is_b": a_is_b
        }
        , "b":{
              "exists": b_exists
            , "empty": b_empty
            , "filename": b_filename
            , "content": b_content
            , "size": len(b_content)
            , "time": b_time
            , "time_delta_s": b_time_delta_s
        }
    }
    # fmt:on
    return ret


def do_battle(item):
    args = {}
    bfn = item.get("b_filename")
    expected_to_be_sane = True
    if item.get("a_exists"):
        args["input"] = item.get("a_filename")
        expected_to_be_sane = False
    if item.get("b_exists"):
        args["output"] = bfn
    p = processor(args, expected_to_be_sane)
    assert p, "No p"
    if expected_to_be_sane:
        success, messages = p.process_files()
        assert success, messages
        if bfn and os.path.exists(bfn):
            item["b"]["processed"] = get_file(bfn)
            item["b"]["processed_size"] = len(item["b"]["processed"])
    return item


def filename_gen(label, base_filename, ext="", a_is_b=False, a_exists=False, a_empty=False, b_exists=False, b_empty=False):
    return f"{label}_{'eq' if a_is_b else 'nq'}_{'aex' if a_exists else 'anx'}_{'bex' if b_exists else 'bnx'}_{'aem' if a_empty else 'anm'}_{'bem' if b_empty else 'bnm'}_{base_filename}{ext}"


def html_name(dt: bool, hs: bool, hd: bool, bs: bool, bd: bool, be: bool, he: bool):
    ret = ""
    ret += "ydt_" if dt else "ndt_"
    ret += "yhs_" if hs else "nhs_"
    ret += "yhd_" if hd else "nhd_"
    ret += "ybs_" if bs else "nbs_"
    ret += "ybd_" if bd else "nbd_"
    ret += "ybe_" if be else "nbe_"
    ret += "yhe" if he else "nhe"
    return ret


def create_test_files(content_pairs, base_filename, ext, base_time=datetime.datetime.now().timestamp()):
    out = []
    b_exists = False
    b_empty = False
    b_time_delta_s = 0
    a_is_b = True
    for a_exists in [True, False]:
        for a_empty in [False, False]:
            for label, content_pair in content_pairs.items():
                a_content, b_content = content_pair
                filename = filename_gen(label, base_filename, ext, a_is_b, a_exists, a_empty, b_exists, b_empty)
                item = create_file_combo(label, base_filename=filename, a_content=a_content, b_content=b_content, base_time=base_time, a_exists=a_exists, b_exists=b_exists, a_is_b=a_is_b, b_time_delta_s=b_time_delta_s)
                out.append(item)
    a_is_b = False
    for b_time_delta_s in [1, 0, -1]:
        for a_exists in [True, False]:
            for b_exists in [True, False]:
                if not a_exists and not b_exists:
                    continue
                for a_empty in [False, True]:
                    for b_empty in [True, False]:
                        for label, content_pair in content_pairs.items():
                            a_content, b_content = content_pair
                            filename = filename_gen(label, base_filename, ext, a_is_b, a_exists, a_empty, b_exists, b_empty)
                            item = create_file_combo(label, base_filename=filename, a_content=a_content, b_content=b_content, base_time=base_time, a_exists=a_exists, b_exists=b_exists, a_is_b=a_is_b, b_time_delta_s=b_time_delta_s)
                            out.append(item)
    return out


def remove_test_files(items, do_debug=False):
    for item in items:
        # logger.info(pprint.pformat(item))
        rm_if_exists(item.get("a", {}).get("filename"), do_debug)
        rm_if_exists(item.get("b", {}).get("filename"), do_debug)


def get_file(fn, is_binary=False, encoding="utf-8"):
    content = ""
    if fn:
        try:
            with open(fn, "rb") if is_binary else open(fn, "r", encoding=encoding) as in_file:
                content = in_file.read()
        except Exception as err:
            # logger.info(f"Could not read from file {fn}: {err}")
            pass
    return content


def files_to_battles(items):
    args = {}
    args["input"] = "./"
    args["output"] = "./"
    p = processor(args)
    assert p, "No p"
    success, messages = p.process_files()
    assert success, messages
    del messages
    del p
    gc.collect()
    for item in items:
        bfn = item.get("b", {}).get("filename")
        item["b"]["processed"] = get_file(bfn)
    return items


def files_to_battles_find_nproc(items, iterations=10, upper=5000, lower=1):
    # Prime the pump with initial discarded run
    nproc_start_time = datetime.datetime.now().timestamp()
    items_copy = copy.deepcopy(files_to_battles(items))
    nproc_last_time = datetime.datetime.now().timestamp() - nproc_start_time
    # Go on the nproc search
    mid = lower
    ct = 0
    while lower <= upper:
        mid = (upper + lower) // 2
        nproc_start_time = datetime.datetime.now().timestamp()
        args = {}
        args["input"] = "./"
        args["output"] = "./"
        args["nproc"] = mid
        p = processor(args)
        assert p, "No p"
        success, messages = p.process_files()
        assert success, messages
        nproc_interval = datetime.datetime.now().timestamp() - nproc_start_time
        if nproc_interval < nproc_last_time:
            logger.info(f"Faster {nproc_interval} with {mid}")
            lower = mid
        elif nproc_interval > nproc_last_time:
            logger.info(f"Slower {nproc_interval} with {mid}")
            upper = mid
        else:
            logger.info(f"Same {nproc_interval} with {mid}")
        nproc_last_time = nproc_interval
        ct += 1
        if ct > iterations:
            break
        del messages
        del p
        gc.collect()
    logger.info(f"Optimal nproc was {nproc_interval} with {mid}")
    return items_copy


def vs_battle(content_pairs):
    out = []
    base_filename = "file_combo.html"
    base_time = start_time
    b_exists = False
    b_empty = False
    b_time_delta_s = 0
    a_is_b = True
    for label, content_pair in content_pairs.items():
        a_content, b_content = content_pair
        for a_exists in [True, False]:
            for a_empty in [True, False]:
                item = create_file_combo(label, base_filename=base_filename, a_content=a_content, b_content=b_content, base_time=base_time, a_exists=a_exists, b_exists=b_exists, a_is_b=a_is_b, b_time_delta_s=b_time_delta_s)
                # Perform battle
                item = do_battle(item)
                # Clean up
                rm_if_exists(item.get("a", {}).get("filename"))
                out.append(item)
    a_is_b = False
    for label, content_pair in content_pairs.items():
        a_content, b_content = content_pair
        for a_exists in [True, False]:
            for b_exists in [True, False]:
                if not a_exists and not b_exists:
                    continue
                for a_empty in [True, False]:
                    for b_empty in [True, False]:
                        for b_time_delta_s in [-1, 0, 1]:
                            item = create_file_combo(label, base_filename=base_filename, a_content=a_content, b_content=b_content, base_time=base_time, a_exists=a_exists, b_exists=b_exists, a_is_b=a_is_b, b_time_delta_s=b_time_delta_s)
                            # Perform battle
                            item = do_battle(item)
                            # Clean up
                            rm_if_exists(item.get("a", {}).get("filename"))
                            rm_if_exists(item.get("b", {}).get("filename"))
                            out.append(item)
    return out


def dict_to_li(d):
    out = "<ul>\n"
    for k, v in d.items():
        out += f"\t<li>{k} = <b>{v}</b></li>\n"
    out += "<ul>\n"
    return out


def battles_to_html(battles):
    title = "Battle"
    out = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>{title}</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/prism.min.js" integrity="sha512-hpZ5pDCF2bRCweL5WoA0/N1elet1KYL5mx3LP555Eg/0ZguaHawxNvEjF6O3rufAChs16HVNhEc6blF/rZoowQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/components/prism-cshtml.min.js" integrity="sha512-bwxCf5C1/8eottG2STXqlH0tqniuL4LwbxdpHebWWqhLywa78nTyd+1o6RLk2BFenAXjtg9wI4bI8M8uHT3bfg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/themes/prism-coy.min.css" integrity="sha512-CKzEMG9cS0+lcH4wtn/UnxnmxkaTFrviChikDEk1MAWICCSN59sDWIF0Q5oDgdG9lxVrvbENSV1FtjLiBnMx7Q==" crossorigin="anonymous" referrerpolicy="no-referrer" />
        <style>
            body *, * {{
                font-family: sans-serif;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <table>
"""
    for item in battles:
        params = copy.deepcopy(item)
        a_params = params["a"]
        b_params = params["b"]
        fna = a_params["filename"]
        fnb = b_params["filename"]
        del a_params["content"]
        del a_params["filename"]
        del b_params["content"]
        del b_params["filename"]
        del b_params["processed"]
        label = item.get("label", "Unknown")
        out += f"<tr><th colspan=6><h2>{label}</h2></th></tr>"
        out += f"""<tr>
    <th><h3>A</h3></th>
    <th>{fna}</th>
    <th><h3>B</h3></th>
    <th>{fnb}</th>
</tr>"""
        a = html.escape(item.get("a", {}).get("content"))
        bd = item.get("b", {})
        b = html.escape(bd.get("processed", "Not found"))
        out += f"""
<tr>
    <td>{dict_to_li(a_params)}</td>
    <td>
        <pre><code class="language-html">{a}</code></pre>
    </td>
    <td>{dict_to_li(b_params)}</td>
    <td>
        <pre><code class="language-html">{b}</code></pre>
    </td>
</tr>
"""
    # out += f"<h2>Raw</h2><pre>{html.escape(pprint.pformat(battles))}</pre>"
    out += "</table></body></html>"
    return out


def html_variant(dt: bool, hs: bool, hd: bool, bs: bool, bd: bool, be: bool, he: bool):
    empty = ""
    ret = ""
    ret += "<!DOCTYPE html>\n" if dt else empty
    ret += "<html>\n" if hs else empty
    ret += "<head><title>Test</title></head>\n" if hd else empty
    ret += "<body>\n" if bs else empty
    ret += "<h1>Test</h1><p>Content</p>\n" if bd else empty
    ret += "</body>\n" if be else empty
    ret += "</html>\n" if he else empty
    return ret
    # return f"{'<!DOCTYPE html>' if dt else ''}{'<html>' if hs else ''}"


# {'<head><title>Test</title></head>\n' if hd else ''}{'<body>\n' if bs else ''}{'<h1>hello</h1><p>Content</p>\n' if bd else ''}{'</body>\n' if be else ''}{'</html>\n' if he else ''}


# return f"{'dt' if dt else '--'}{'hs' if hs else '--'}{'hd' if hd else '--'}"


# {'bs' if bs else '--'}{'bd' if bd else '--'}{'be' if be else '--'}{'he' if he else '--'}


def html_variants():
    out = {}
    for html_start_tag in [False, True]:
        for html_end_tag in [False, True]:
            for body_end_tag in [False, True]:
                for body_content in [True, False]:
                    for doctype in [False, True]:
                        for head_tag in [False, True]:
                            for body_start_tag in [False, True]:
                                name = html_name(doctype, html_start_tag, head_tag, body_start_tag, body_content, body_end_tag, html_end_tag)
                                # f"{""doctype}{html_start_tag}{head_tag}{body_start_tag}{body_content}{body_end_tag}{html_end_tag}"
                                out[name] = html_variant(doctype, html_start_tag, head_tag, body_start_tag, body_content, body_end_tag, html_end_tag)
    return out


def print_results(p, name):
    out, msg = p
    logger.info(name)
    logger.info("\n\n" + out + "\n")
    logger.info("\n\n" + pprint.pformat(msg))


def test_webparser():
    go_into_test_dir("")
    webparser = web_minify.handlers.html.webparser.WebParser()

    for fn in ["parser_test.html", "parser_test2.html"]:
        f = get_file(fn)
        webparser.parse(f)
        print_results(webparser.beautify(), f"BEAUTIFY({fn}, {len(f)} bytes)")
        # print_results(webparser.minify(), "MINIFY({fn}, {len(f)} bytes)")
        # print_results(webparser.debugify(), "DEBUGIFY({fn}, {len(f)} bytes)")


def _test_processor_html():
    go_into_test_dir()
    variants = html_variants()
    variants["none"] = "<div>test</div>"
    content_pairs = {}
    for k, v in variants.items():
        content_pairs[k] = (v, v)
    files = create_test_files(content_pairs, "test", ".html", base_time=start_time)
    battles = files_to_battles(files)
    # battles = files_to_battles_find_nproc(items=files, iterations=10, upper=150, lower=90)
    remove_test_files(files)
    # battles = vs_battle(content_pairs)
    create_dummy_file("../report.html", battles_to_html(battles))


def processor(args={}, expected_to_be_sane=True):
    # fmt:off
    defaults = {
          "format": ""
        , "mode": "beautify"
        , "overwrite": True
        , "on_change": False
        , "verbose": False
        , "quiet": False
        , "gzip": False
        , "sort": False
        , "comments": False
        , "timestamp": False
        , "wrap": False
        , "nproc":120
        , "no_size_checks": True
    }
    # fmt:on
    settings = {**defaults, **args}
    p = web_minify.processor.Processor(settings)
    sane, message = p.sanity_checks()
    assert expected_to_be_sane, message
    return p


def _test_processor_js():
    now = start_time

    existant_input_fn = "existant_input.js"
    existant_input_content = "existant_content"
    existant_input_mtime = create_dummy_file(existant_input_fn, existant_input_content)

    existant_input_empty_fn = "existant_input_empty.js"
    existant_input_empty_content = ""
    existant_input_empty_mtime = create_dummy_file(existant_input_empty_fn, existant_input_empty_content)

    existant_output_older_fn = "existant_output_older.js"
    existant_output_older_content = ""
    existant_output_older_mtime = existant_input_mtime - 100
    assert existant_output_older_mtime == create_dummy_file(existant_output_older_fn, existant_output_older_content, existant_output_older_mtime)

    existant_output_same_fn = "existant_input_same.js"
    existant_output_same_content = ""
    existant_output_same_mtime = existant_input_mtime
    assert existant_output_same_mtime == create_dummy_file(existant_output_same_fn, existant_output_same_content, existant_output_same_mtime)

    existant_output_newer_fn = "existant_input_newer.js"
    existant_output_newer_content = ""
    existant_output_newer_mtime = existant_input_mtime + 100
    assert existant_output_newer_mtime == create_dummy_file(existant_output_newer_fn, existant_output_newer_content, existant_output_newer_mtime)

    args = {"input": "inexistant_input.js"}
    p = processor(args, False)

    args = {"input": existant_input_fn}
    p = processor(args)

    success, status, messages = p.process_file(input_path=existant_input_fn, output_path=existant_output_same_fn)
    assert success, messages
    assert not status.get("copied"), messages
    assert status.get("skipped"), messages

    success, status, message = p.process_file(input_path=existant_input_fn, output_path=existant_output_older_fn)
    assert success, messages
    assert not status.get("copied"), messages
    assert not status.get("skipped"), messages

    success, status, message = p.process_file(input_path=existant_input_fn, output_path=existant_output_newer_fn)
    assert success, messages
    assert not status.get("copied"), messages
    assert status.get("skipped"), messages
