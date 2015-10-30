from argparse import ArgumentParser
from pipelines import nb, script
import os
import logging
import pprint
from jinja2 import Environment, FileSystemLoader


logger = logging.getLogger(__name__)
streamhandler = logging.StreamHandler()
logger.addHandler(streamhandler)


notebooks_path = nb.__path__._path[0]
notebook_names = [os.path.splitext(name)[0] for name in os.listdir(notebooks_path)]


scripts_path = script.__path__._path[0]
script_names = [os.path.splitext(name)[0] for name in os.listdir(scripts_path)]


def main():
    p = ArgumentParser(
        description="Automagically generate an analysis pipeline given a uid!",
    )

    p.add_argument(
        '-o', '--output-dir',
        action='store',
        nargs='?',
        help='Output directory for the analysis pipeline',
        default='.',
    )

    p.add_argument(
        'uid',
        action='store',
        help='A valid identifier for the scan. See db[] syntax',
    )

    p.add_argument(
        'pipeline',
        action='store',
        help='The type of pipeline to create.'
    )

    p.add_argument(
        '-n', '--notebook',
        action='store_true',
        default=True,
        help='Generate a notebook pipeline. Valid notebooks are %s' % notebook_names
    )

    p.add_argument(
        '-s', '--script',
        action='store_true',
        default=False,
        help='Generate a script pipeline. Valid scripts are %s' % script_names,
    )

    p.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Sets log level to INFO'
    )

    p.add_argument(
        '-vv', '--very-verbose',
        action='store_true',
        help='Sets log level to DEBUG'
    )

    p.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Turn off logging'
    )

    args = p.parse_args()

    loglevel = logging.WARN
    if args.verbose:
        loglevel = logging.INFO
    elif args.very_verbose:
        loglevel = logging.DEBUG
    elif args.quiet:
        logger.removeHandler(streamhandler)

    logger.setLevel(loglevel)
    streamhandler.setLevel(loglevel)
    logger.info('\nvalid_notebooks'
                '\n---------------')
    logger.info(pprint.pformat(notebooks_path))
    logger.info('\nParsed Arguments'
                '\n----------------')
    logger.info(args)

    execute_programmatically(**vars(args))


def execute_programmatically(uid, pipeline, output_dir, notebook=None, script=None, **args):

    if notebook:
        template_dir = notebooks_path
        suffix = '.ipynb'
    elif script:
        template_dir = scripts_path
        suffix = '.py'
    else:
        raise ValueError("You must supply `notebook` or `script` as a kwarg")

    logger.info("Template directory = %s" % template_dir)
    jinja_env = Environment(loader=FileSystemLoader(template_dir))

    output_path = os.path.join(output_dir, pipeline+suffix)
    logger.info("Writing to %s" % output_path)

    template_name = '%s.tmpl' % pipeline
    logger.info("Loading template = %s" % template_name)

    template = jinja_env.get_template(template_name)
    template_info = {'uid': uid}
    pipeline = template.render(**template_info)
    with open(output_path, 'w') as f:
        f.write(pipeline)
