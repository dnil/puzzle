# -*- coding: utf-8 -*-
import logging

import click

import puzzle
from .factory import create_app
from .log import configure_stream, LEVELS
from .plugins import VcfPlugin
from .settings import BaseConfig

logger = logging.getLogger(__name__)


@click.group()
@click.option('-t', '--plugin', type=click.Choice(['vcf']), default='vcf')
@click.option('-v', '--verbose', count=True, default=2)
@click.argument('root')
@click.pass_context
def cli(ctx, plugin, verbose, root):
    """Puzzle: manage DNA variant resources."""
    # configure root logger to print to STDERR
    loglevel = LEVELS.get(min(verbose, 3))
    configure_stream(level=loglevel)

    # launch the command line interface
    logger.debug('Booting up command line interface')
    ctx.root = root

    if plugin == 'vcf':
        ctx.plugin = VcfPlugin()


@cli.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000)
@click.option('--debug', is_flag=True)
@click.option('-p', '--pattern', default='*.vcf')
@click.version_option(puzzle.__version__)
@click.pass_context
def view(ctx, host, port, debug, pattern):
    """Visualize DNA variant resources."""
    BaseConfig.PUZZLE_ROOT = ctx.parent.root
    BaseConfig.PUZZLE_PATTERN = pattern
    BaseConfig.PUZZLE_BACKEND = ctx.parent.plugin
    app = create_app(config_obj=BaseConfig)
    app.run(host=host, port=port, debug=debug)