from .exception import FuzzExceptBadRecipe, FuzzExceptBadOptions, FuzzExceptBadFile
from .facade import Facade, ERROR_CODE, BASELINE_CODE

from .fuzzobjects import FuzzStats
from .filter import FuzzResFilter
from .core import requestGenerator
from .utils import (
    json_minify,
    python2_3_convert_from_unicode,
)

from .core import Fuzzer
from .myhttp import HttpPool

from .externals.reqresp.cache import HttpCache

from collections import defaultdict

# python 2 and 3
try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict

import json


class FuzzSession(UserDict):
    def __init__(self, **kwargs):
        self.data = self._defaults()
        self.keys_not_to_dump = ["interactive", "recipe", "seed_payload", "send_discarded", "compiled_genreq", "compiled_filter", "compiled_prefilter", "compiled_printer", "description", "show_field"]

        # recipe must be superseded by options
        if "recipe" in kwargs and kwargs["recipe"]:
            for recipe in kwargs["recipe"]:
                self.import_from_file(recipe)

        self.update(kwargs)

        self.cache = HttpCache()
        self.http_pool = None

        self.stats = FuzzStats()

    def _defaults(self):
        return dict(
            send_discarded=False,
            console_printer="",
            hs=None,
            hc=[],
            hw=[],
            hl=[],
            hh=[],
            ss=None,
            sc=[],
            sw=[],
            sl=[],
            sh=[],
            payloads=None,
            iterator=None,
            printer=(None, None),
            colour=False,
            previous=False,
            verbose=False,
            interactive=False,
            dryrun=False,
            recipe=[],
            save="",
            proxies=None,
            conn_delay=int(Facade().sett.get('connection', 'conn_delay')),
            req_delay=int(Facade().sett.get('connection', 'req_delay')),
            retries=int(Facade().sett.get('connection', 'retries')),
            rlevel=0,
            scanmode=False,
            delay=None,
            concurrent=int(Facade().sett.get('connection', 'concurrent')),
            url="",
            method=None,
            auth=(None, None),
            follow=False,
            postdata=None,
            headers=[],
            cookie=[],
            allvars=None,
            script="",
            script_args={},
            connect_to_ip=None,
            description=None,
            no_cache=False,
            show_field=None,

            # this is equivalent to payloads but in a different format
            dictio=None,

            # these will be compiled
            seed_payload=False,
            filter="",
            prefilter="",
            compiled_genreq=None,
            compiled_filter=None,
            compiled_prefilter=None,
            compiled_printer=None,
        )

    def update(self, options):
        self.data.update(options)

    def validate(self):
        error_list = []

        if self.data['dictio'] and self.data['payloads']:
            raise FuzzExceptBadOptions("Bad usage: Dictio and payloads options are mutually exclusive. Only one could be specified.")

        if self.data['rlevel'] > 0 and self.data['dryrun']:
            error_list.append("Bad usage: Recursion cannot work without making any HTTP request.")

        if self.data['script'] and self.data['dryrun']:
            error_list.append("Bad usage: Plugins cannot work without making any HTTP request.")

        if self.data['no_cache'] not in [True, False]:
            raise FuzzExceptBadOptions("Bad usage: No-cache is a boolean value")

        if not self.data['url']:
            error_list.append("Bad usage: You must specify an URL.")

        if not self.data['payloads'] and not self.data["dictio"]:
            error_list.append("Bad usage: You must specify a payload.")

        if self.data["hs"] and self.data["ss"]:
            raise FuzzExceptBadOptions("Bad usage: Hide and show regex filters flags are mutually exclusive. Only one could be specified.")

        if self.data["rlevel"] < 0:
            raise FuzzExceptBadOptions("Bad usage: Recursion level must be a positive int.")

        if self.data['allvars'] not in [None, 'allvars', 'allpost', 'allheaders']:
            raise FuzzExceptBadOptions("Bad options: Incorrect all parameters brute forcing type specified, correct values are allvars,allpost or allheaders.")

        if self.data['proxies']:
            for ip, port, ttype in self.data['proxies']:
                if ttype not in ("SOCKS5", "SOCKS4", "HTTP"):
                    raise FuzzExceptBadOptions("Bad proxy type specified, correct values are HTTP, SOCKS4 or SOCKS5.")

        try:
            if [x for x in ["sc", "sw", "sh", "sl"] if len(self.data[x]) > 0] and \
               [x for x in ["hc", "hw", "hh", "hl"] if len(self.data[x]) > 0]:
                raise FuzzExceptBadOptions("Bad usage: Hide and show filters flags are mutually exclusive. Only one group could be specified.")

            if ([x for x in ["sc", "sw", "sh", "sl"] if len(self.data[x]) > 0] or
               [x for x in ["hc", "hw", "hh", "hl"] if len(self.data[x]) > 0]) and \
               self.data['filter']:
                raise FuzzExceptBadOptions("Bad usage: Advanced and filter flags are mutually exclusive. Only one could be specified.")
        except TypeError:
            raise FuzzExceptBadOptions("Bad options: Filter must be specified in the form of [int, ... , int].")

        return error_list

    def export_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write(self.export_json())
        except IOError:
            raise FuzzExceptBadFile("Error writing recipe file.")

    def import_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                self.import_json(f.read())
        except IOError:
            raise FuzzExceptBadFile("Error loading recipe file.")

    def import_json(self, data):
        js = json.loads(json_minify(data))

        try:
            if js['version'] == "0.2" and 'wfuzz_recipe' in js:
                for section in js['wfuzz_recipe'].keys():
                    for k, v in js['wfuzz_recipe'].items():
                        if k not in self.keys_not_to_dump:
                            # python 2 and 3 hack
                            self.data[k] = python2_3_convert_from_unicode(v)
            else:
                raise FuzzExceptBadRecipe("Unsupported recipe version.")
        except KeyError:
            raise FuzzExceptBadRecipe("Incorrect recipe format.")

    def export_json(self):
        tmp = dict(
            version="0.2",
            wfuzz_recipe=defaultdict(dict)
        )
        defaults = self._defaults()

        # Only dump the non-default options
        for k, v in self.data.items():
            if v != defaults[k] and k not in self.keys_not_to_dump:
                tmp['wfuzz_recipe'][k] = self.data[k]

        return json.dumps(tmp, sort_keys=True, indent=4, separators=(',', ': '))

    def payload(self, **kwargs):
        try:
            self.data.update(kwargs)
            self.data['compiled_genreq'] = requestGenerator(self)
            for r in self.data['compiled_genreq'].get_dictio():
                yield r
        finally:
            self.data['compiled_genreq'].close()

    def fuzz(self, **kwargs):
        self.data.update(kwargs)

        fz = None
        try:
            fz = Fuzzer(self.compile())

            for f in fz:
                yield f

        finally:
            if fz:
                fz.cancel_job()
                self.stats.update(fz.genReq.stats)

            if self.http_pool:
                self.http_pool.deregister()
                self.http_pool = None

    def get_payloads(self, iterator):
        self.data["dictio"] = iterator

        return self

    def get_payload(self, iterator):
        return self.get_payloads([iterator])

    def __enter__(self):
        self.http_pool = HttpPool(self)
        self.http_pool.register()
        return self

    def __exit__(self, *args):
        self.close()

    def compile(self):
        # Validate options
        error = self.validate()
        if error:
            raise FuzzExceptBadOptions(error[0])

        self.data["seed_payload"] = True if self.data["url"] == "FUZZ" else False

        # printer
        try:
            filename, printer = self.data["printer"]
        except ValueError:
            raise FuzzExceptBadOptions("Bad options: Printer must be specified in the form of ('filename', 'printer')")

        if filename:
            if printer == "default" or not printer:
                printer = Facade().sett.get('general', 'default_printer')
            self.data["compiled_printer"] = Facade().printers.get_plugin(printer)(filename)

        try:
            self.data['hc'] = [BASELINE_CODE if i == "BBB" else ERROR_CODE if i == "XXX" else int(i) for i in self.data['hc']]
            self.data['hw'] = [BASELINE_CODE if i == "BBB" else ERROR_CODE if i == "XXX" else int(i) for i in self.data['hw']]
            self.data['hl'] = [BASELINE_CODE if i == "BBB" else ERROR_CODE if i == "XXX" else int(i) for i in self.data['hl']]
            self.data['hh'] = [BASELINE_CODE if i == "BBB" else ERROR_CODE if i == "XXX" else int(i) for i in self.data['hh']]

            self.data['sc'] = [BASELINE_CODE if i == "BBB" else ERROR_CODE if i == "XXX" else int(i) for i in self.data['sc']]
            self.data['sw'] = [BASELINE_CODE if i == "BBB" else ERROR_CODE if i == "XXX" else int(i) for i in self.data['sw']]
            self.data['sl'] = [BASELINE_CODE if i == "BBB" else ERROR_CODE if i == "XXX" else int(i) for i in self.data['sl']]
            self.data['sh'] = [BASELINE_CODE if i == "BBB" else ERROR_CODE if i == "XXX" else int(i) for i in self.data['sh']]
        except ValueError:
            raise FuzzExceptBadOptions("Bad options: Filter must be specified in the form of [int, ... , int, BBB, XXX].")

        # filter options
        self.data["compiled_filter"] = FuzzResFilter.from_options(self)
        self.data["compiled_prefilter"] = FuzzResFilter(filter_string=self.data['prefilter'])

        # seed
        self.data["compiled_genreq"] = requestGenerator(self)

        # Check payload num
        fuzz_words = self.data["compiled_filter"].get_fuzz_words() + self.data["compiled_prefilter"].get_fuzz_words() + self.data["compiled_genreq"].get_fuzz_words()

        if self.data['allvars'] is None and len(set(fuzz_words)) == 0:
            raise FuzzExceptBadOptions("You must specify at least a FUZZ word!")

        if self.data["compiled_genreq"].baseline is None and (BASELINE_CODE in self.data['hc'] or
           BASELINE_CODE in self.data['hl'] or BASELINE_CODE in self.data['hw'] or
           BASELINE_CODE in self.data['hh']):
            raise FuzzExceptBadOptions("Bad options: specify a baseline value when using BBB")

        if self.data["script"]:
            Facade().scripts.kbase.update(self.data["script_args"])

            for k, v in Facade().sett.get_section("kbase"):
                if k not in self.data["script_args"]:
                    Facade().scripts.kbase[k] = v

        if not self.http_pool:
            self.http_pool = HttpPool(self)
            self.http_pool.register()

        return self

    def close(self):
        if self.http_pool:
            self.http_pool.deregister()
            self.http_pool = None
