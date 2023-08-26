"""
Loads trigger modules listed in config.py

Stores utility functions available to every trigger in folder
"""

import logging
logger = logging.getLogger(__name__)

import os
from importlib import import_module
from rataGUI import launch_config

enabled_triggers = launch_config.get("Enabled Trigger Modules")
if enabled_triggers is not None:
    for module_name in enabled_triggers:
        try:
            abs_module_path = f"{__name__}.{module_name}"
            import_module(abs_module_path)
            logger.info(f"Loaded trigger module: {module_name}.py")
        except ImportError as err:
            logger.warning(f"Unable to load trigger module: {module_name}.py")
            logger.error(err.msg)
        except Exception as err:
            logger.exception(err)

else: # Load all modules if launch config does not specify 
    for fname in os.listdir(os.path.dirname(__file__)):
        # Load only "real modules"
        if not fname.startswith('.') and not fname.startswith('__') and fname.endswith('.py'):
            try:
                abs_module_path = f"{__name__}.{fname[:-3]}"
                import_module(abs_module_path)
                logger.info(f"Loaded trigger module: {fname}")
            except ImportError as err:
                logger.warning(f"Unable to load trigger module: {fname}")
                logger.error(err.msg)
            except Exception as err:
                logger.exception(err)