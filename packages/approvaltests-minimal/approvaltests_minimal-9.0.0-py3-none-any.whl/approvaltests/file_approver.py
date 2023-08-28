import filecmp
import os
import pathlib
from typing import Optional

from approvaltests.core.comparator import Comparator
from approvaltests.core.namer import Namer
from approvaltests.core.reporter import Reporter
from approvaltests.core.writer import Writer


def exists(path: str) -> bool:
    return os.path.isfile(path)


class ReporterNotWorkingException(Exception):
    def __init__(self, reporter: Reporter):
        super().__init__(f"Reporter {reporter} failed to work!")


class FileComparator(Comparator):
    def compare(self, received_path: str, approved_path: str) -> bool:
        if not exists(approved_path) or not exists(received_path):
            return False
        if filecmp.cmp(approved_path, received_path):
            return True
        try:
            approved_raw = pathlib.Path(approved_path).read_text()
            approved_text = approved_raw.replace("\r\n", "\n")
            received_raw = pathlib.Path(received_path).read_text()
            received_text = received_raw.replace("\r\n", "\n")
            return approved_text == received_text
        except BaseException:
            return False


class FileApprover:
    @staticmethod
    def verify(
        namer: Namer, writer: Writer, reporter: Reporter, comparator: Comparator
    ) -> Optional[str]:
        approved = namer.get_approved_filename()
        received = namer.get_received_filename()

        # The writer has the ability to change the name of the received file
        received = writer.write_received_file(received)
        verified = FileApprover.verify_files(approved, received, reporter, comparator)

        if not verified:
            return (
                f"Approval Mismatch, received != approved\n"
                f"\tApproved: {approved}\n"
                f"\tReceived: {received} "
            )
        return None

    @staticmethod
    def verify_files(
        approved_file: str,
        received_file: str,
        reporter: Reporter,
        comparator: Comparator,
    ) -> bool:
        if comparator.compare(received_file, approved_file):
            os.remove(received_file)
            return True

        worked = reporter.report(received_file, approved_file)
        if not worked:
            raise ReporterNotWorkingException(reporter)
        return False
