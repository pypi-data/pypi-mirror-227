"""
database.py - Create and manage a tclRAL database
"""

import logging
import tkinter
from pyral.transaction import Transaction
from pathlib import Path

class Database:
    """
    Proxy for a tclRAL database.

    First we must initiate the connection with an optionally specified database.
    If none is specified, a new in memory database may be created

    """
    _logger = logging.getLogger(__name__)
    tclRAL = None  # Tcl interpreter
    transaction = None
    init_script_path = str(Path(__file__).parent / "tcl_scripts" / "init_TclRAL.tcl")

    @classmethod
    def init(cls, db_path=None):
        """
        Get a tcl interpreter and run a script in it that loads up TclRAL
        :return:
        """
        cls.tclRAL = tkinter.Tcl()  # Got tcl interpreter
        # Load TclRAL into that interpreter
        cls.tclRAL.eval(f"source {cls.init_script_path}")
        cls._logger.info("TclRAL initiated")

        if db_path:
            # TODO: Have TclRAL load the tclral from the specified path
            pass
        return cls.tclRAL

    @classmethod
    def open_transaction(cls):
        """

        :return:
        """
        Transaction.open(tclral=cls.tclRAL)

    @classmethod
    def save(cls, fname):
        """
        Save the db in the supplied file
        """
        cls.tclRAL.eval(f"serializeToFile {fname}")

    @classmethod
    def load(cls, fname):
        """
        Load the db from the supplied file
        """
        cls.tclRAL.eval(f"deserializeFromFile {fname}")

    @classmethod
    def names(cls, pattern: str = ""):
        """
        Use this to obtain names of all created relvars or those specified by the optional pattern.

        :param pattern:
        """
        result = cls.tclRAL.eval(f"relvar names {pattern}")
        cls._logger.info(result)

    @classmethod
    def constraint_names(cls, pattern: str = ""):
        """
        Use this to obtain names of all created constraints or those specified by the optional pattern.

        :param pattern:
        """
        result = cls.tclRAL.eval(f"relvar constraint names {pattern}")
        cls._logger.info(result)

