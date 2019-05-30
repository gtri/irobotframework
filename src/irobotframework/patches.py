# Copyright (c) 2018 Georgia Tech Research Corporation
# Distributed under the terms of the BSD-3-Clause License

# Derived from robotkernel
# Copyright (c) 2018, Asko Soukka
# Distributed under the terms of the BSD-3-Clause License

""" Various dirty patches
"""
# from warnings import warn
import asyncio
import sys
import types


class ScopedCodeRunner(object):
    """ Patch an shell to execute code in a sys.module

        Robot Framework only looks in sys.modules
    """

    def __init__(self, shell, module_name):
        self.shell = shell
        self.module_name = module_name
        self._run_code_backup = shell.run_code

    def __enter__(self):
        if self.module_name not in sys.modules:
            sys.modules[self.module_name] = types.ModuleType(self.module_name)

        _module = sys.modules[self.module_name]

        @asyncio.coroutine
        def run_code(self, code_obj, result=None, *, async_=False):
            """Execute a code object.

            When an exception occurs, self.showtraceback() is called to display a
            traceback.

            Parameters
            ----------
            code_obj : code object
              A compiled code object, to be executed
            result : ExecutionResult, optional
              An object to store exceptions that occur during execution.
            async_ :  Bool (Experimental)
              Attempt to run top-level asynchronous code in a default loop.

            Returns
            -------
            False : successful execution.
            True : an error occurred.
            """
            # pylint: disable=W0702,W0122,C0103
            # flake8: noqa
            # Set our own excepthook in case the user code tries to call it
            # directly, so that the IPython crash handler doesn't get triggered
            old_excepthook, sys.excepthook = sys.excepthook, self.excepthook

            # we save the original sys.excepthook in the instance, in case config
            # code (such as magics) needs access to it.
            self.sys_excepthook = old_excepthook
            outflag = True  # happens in more places, so it's easier as default
            try:
                try:
                    self.hooks.pre_run_code_hook()
                    if async_:
                        last_expr = (
                            yield from self._async_exec(code_obj, self.user_ns)
                        )
                        code = compile("last_expr", "fake", "single")
                        exec(code, {"last_expr": last_expr})
                    else:
                        exec(code_obj, _module.__dict__)
                finally:
                    # Reset our crash handler in place
                    sys.excepthook = old_excepthook
            except SystemExit as e:
                if result is not None:
                    result.error_in_exec = e
                self.showtraceback(exception_only=True)
                # warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)
            except self.custom_exceptions:
                etype, value, tb = sys.exc_info()
                if result is not None:
                    result.error_in_exec = value
                self.CustomTB(etype, value, tb)
            except:
                if result is not None:
                    result.error_in_exec = sys.exc_info()[1]
                self.showtraceback(running_compiled_code=True)
            else:
                outflag = False
            return outflag

        self.shell.run_code = types.MethodType(run_code, self.shell)

    def __exit__(self, *exc):
        self.shell.run_code = self._run_code_backup
