"""SCons.Tool.midl

Tool-specific initialization for midl (Microsoft IDL compiler).

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import string

import parts.api.output as output
import parts.tools.Common
import SCons.Action
import SCons.Builder
import SCons.Defaults
import SCons.Scanner.IDL
import SCons.Util
from parts.tools.MSCommon import msvc

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"


def midl_emitter(target, source, env):
    """Produces a list of outputs from the MIDL compiler"""
    base, ext = SCons.Util.splitext(str(target[0]))
    tlb = target[0]
    incl = base + '.h'
    interface = base + '_i.c'
    t = [tlb, incl, interface]

    midlcom = env['MIDLCOM']

    if midlcom.find('/proxy') != -1:
        proxy = base + '_p.c'
        t.append(proxy)
    if midlcom.find('/dlldata') != -1:
        dlldata = base + '_data.c'
        t.append(dlldata)

    return (t, source)


idl_scanner = SCons.Scanner.IDL.IDLScan()

midl_action = SCons.Action.Action('$MIDLCOM', '$MIDLCOMSTR')

midl_builder = SCons.Builder.Builder(action=midl_action,
                                     src_suffix='.idl',
                                     suffix='.tlb',
                                     emitter=midl_emitter,
                                     source_scanner=idl_scanner)


def generate(env):
    """Add Builders and construction variables for midl to an Environment."""

    msvc.MergeShellEnv(env)
    env['MIDL'] = parts.tools.Common.toolvar('midl', ('mild',), env=env)
    env['MIDLFLAGS'] = SCons.Util.CLVar('/nologo')
    env['MIDLCOM'] = '$MIDL $MIDLFLAGS /tlb ${TARGETS[0]} /h ${TARGETS[1]} /iid ${TARGETS[2]} /proxy ${TARGETS[3]} /dlldata ${TARGETS[4]} $SOURCE'
    env['BUILDERS']['TypeLibrary'] = midl_builder
    #api.output.print_msg("Configured Tool %s\t for version <%s> target <%s>"%('midl',env['MSVC']['VERSION'],env['TARGET_PLATFORM']))


def exists(env):
    return msvc.Exists(env, 'midl')

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
