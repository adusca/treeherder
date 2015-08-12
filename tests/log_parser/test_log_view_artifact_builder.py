import pytest
from mock import MagicMock

from tests import test_utils
from treeherder.log_parser.artifactbuildercollection import ArtifactBuilderCollection
from treeherder.log_parser.artifactbuilders import BuildbotLogViewArtifactBuilder
from treeherder.log_parser.parsers import ErrorParser

from ..sampledata import SampleData

slow = pytest.mark.slow


def do_test(log, check_errors=True):
    """
    Test a single log.

    ``log`` - the url prefix of the log to test.  Also searches for the
              result file with the same prefix.
    """

    url = "file://{0}".format(
        SampleData().get_log_path("{0}.txt.gz".format(log)))

    builder = BuildbotLogViewArtifactBuilder(url, check_errors=check_errors)
    lpc = ArtifactBuilderCollection(url, builders=builder)
    lpc.parse()
    act = lpc.artifacts[builder.name]

    # we can't compare the "logurl" field, because it's a fully qualified url,
    # so it will be different depending on the config it's run in.
    assert "logurl" in act
    del(act["logurl"])

    exp = test_utils.load_exp("{0}.logview.json".format(log))

    # :: use to create the ``exp`` files, if you're making a lot of them
    # with open(SampleData().get_log_path("{0}.logview.json".format(log)), "w") as f:
    #     f.write(json.dumps(act, indent=4))

    # log urls won't match in tests, since they're machine specific
    # but leave it in the exp file as an example of what the real structure
    # should look like.
    del(exp["logurl"])

    assert act == exp  # , diff(exp, act)

    # :: Use this assert when creating new tests and you want to get the actual
    # returned artifact:
    # assert act == exp, json.dumps(act, indent=4)


def test_crashtest_passing(initial_data):
    """Process a job with a single log reference."""

    do_test(
        "mozilla-central_fedora-b2g_test-crashtest-1-bm54-tests1-linux-build50"
    )


def test_mochitest_pass(initial_data):
    """Process a job with a single log reference."""

    do_test(
        "mozilla-central_mountainlion_test-mochitest-2-bm77-tests1-macosx-build141"
    )


def test_duration_gt_1hr(initial_data):
    do_test(
        "mozilla-central-win32-pgo-bm85-build1-build111"
    )


@slow
def test_mochitest_fail(initial_data):
    """Process a job with a single log reference."""

    do_test(
        "mozilla-esr17_xp_test_pgo-mochitest-browser-chrome-bm74-tests1-windows-build12"
    )


def test_mochitest_process_crash(initial_data):
    """Test a mochitest log that has PROCESS-CRASH """

    do_test(
        "mozilla-inbound_ubuntu64_vm-debug_test-mochitest-other-bm53-tests1-linux-build122"
    )


@slow
def test_jetpack_fail(initial_data):
    """Process a job with a single log reference."""

    do_test(
        "ux_ubuntu32_vm_test-jetpack-bm67-tests1-linux-build16"
    )


@slow
def test_crash_1(initial_data):
    """Test from old log parser"""
    do_test(
        "crash-1"
    )


@slow
def test_crash_2(initial_data):
    """Test from old log parser"""
    do_test(
        "crash-2"
    )


@slow
def test_crash_mac_1(initial_data):
    """Test from old log parser"""
    do_test(
        "crash-mac-1"
    )


@slow
def test_crashtest_timeout(initial_data):
    """Test from old log parser"""
    do_test(
        "crashtest-timeout"
    )


@slow
def test_jsreftest_fail(initial_data):
    """Test from old log parser"""
    do_test(
        "jsreftest-fail"
    )


@slow
def test_jsreftest_timeout_crash(initial_data):
    """Test from old log parser"""
    do_test(
        "jsreftest-timeout-crash"
    )


@slow
def test_leaks_1(initial_data):
    """Test from old log parser"""
    do_test(
        "leaks-1"
    )


@slow
def test_mochitest_test_end(initial_data):
    """Test from old log parser"""
    do_test(
        "mochitest-test-end"
    )


@slow
def test_multiple_timeouts(initial_data):
    """Test from old log parser"""
    do_test(
        "multiple-timeouts"
    )


@slow
def test_opt_objc_exception(initial_data):
    """Test from old log parser"""
    do_test(
        "opt-objc-exception"
    )


@slow
def test_reftest_fail_crash(initial_data):
    """Test from old log parser"""
    do_test(
        "reftest-fail-crash"
    )


@slow
def test_reftest_jserror(initial_data):
    """Test from old log parser"""
    do_test(
        "reftest-jserror"
    )


@slow
def test_reftest_opt_fail(initial_data):
    """Test from old log parser"""
    do_test(
        "reftest-opt-fail"
    )


@slow
def test_reftest_timeout(initial_data):
    """Test from old log parser"""
    do_test(
        "reftest-timeout"
    )


@slow
def test_tinderbox_exception(initial_data):
    """Test from old log parser"""
    do_test(
        "tinderbox-exception"
    )


def test_xpcshell_crash(initial_data):
    """Test from old log parser"""
    do_test(
        "xpcshell-crash"
    )


def test_xpcshell_multiple(initial_data):
    """Test from old log parser"""
    do_test(
        "xpcshell-multiple"
    )


def test_xpcshell_timeout(initial_data):
    """Test from old log parser"""
    do_test(
        "xpcshell-timeout"
    )


def test_extreme_log_line_length_truncation(initial_data):
    """This log has lines that are huge.  Ensure we truncate the lines to 100"""
    do_test(
        "mozilla-central_ubuntu64_hw_test-androidx86-set-4-bm103-tests1-linux-build369"
    )


def test_too_many_error_lines_truncation(initial_data):
    """This log has a large number of lines that match the error regex. Ensure we truncate to 100 lines."""
    do_test(
        "large-number-of-error-lines"
    )


@slow
def test_check_errors_false(initial_data, monkeypatch):
    """ensure that parse_line is not called on the error parser."""

    mock_pl = MagicMock(name="parse_line")
    monkeypatch.setattr(ErrorParser, 'parse_line', mock_pl)

    do_test(
        "mozilla-central_mountainlion_test-mochitest-2-bm77-tests1-macosx-build141",
        check_errors=False
    )
    assert mock_pl.called is False


def test_check_errors_true(initial_data, monkeypatch):
    """ensure that parse_line is called on the error parser."""

    mock_pl = MagicMock(name="parse_line")
    monkeypatch.setattr(ErrorParser, 'parse_line', mock_pl)

    do_test(
        "mozilla-central_mountainlion_test-mochitest-2-bm77-tests1-macosx-build141"
    )
    assert mock_pl.called is True
