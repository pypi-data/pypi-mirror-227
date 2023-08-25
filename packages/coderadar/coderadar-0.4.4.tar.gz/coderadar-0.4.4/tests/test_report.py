from __future__ import absolute_import

import pytest



def test_Report():
    from coderadar.report import Report
    my_report = Report()
    assert isinstance(my_report, Report)

def test_summarizeCodeQuality_previousPylintEmpty(mocker):
    mock_CoverageReport = mocker.patch('coderadar.pytest.CoverageReport.__init__')
    mock_CoverageReport.return_value = None
    mock_PylintReport = mocker.patch('coderadar.pylint.PylintReport.__init__')
    mock_PylintReport.side_effect = [None,
                                     RuntimeError("File 'last_run/pylint.json' is empty!")]
    mock_exists = mocker.patch('os.path.exists')
    mock_exists.return_value = True

    mock_CoverageReport = mocker.patch('coderadar.report.Report.getReportTemplate')
    mock_CoverageReport.return_value = 'blubb'
    mock_CoverageReport = mocker.patch('coderadar.report.Report._fillTemplate')
    mock_CoverageReport.return_value = 'blubb'

    mock_open = mocker.patch('builtins.open')

    from coderadar.report import Report
    my_report = Report()
    my_report.summarizeCodeQuality('my_module')
