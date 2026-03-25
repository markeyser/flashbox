import pytest
from unittest.mock import MagicMock
from flashbox.cli import main

@pytest.fixture
def mock_dependencies(mocker):
    """Mocks out the DockerManager and FlashboxMonitor completely to isolate the CLI router."""
    mock_manager_class = mocker.patch("flashbox.cli.DockerManager")
    mock_manager_instance = mock_manager_class.return_value
    
    # We patch the monitor class too to avoid it initializing a Real rich UI
    mock_monitor_class = mocker.patch("flashbox.cli.FlashboxMonitor")
    mock_monitor_instance = mock_monitor_class.return_value
    
    return mock_manager_instance, mock_monitor_class, mock_monitor_instance

def test_cli_start(mocker, mock_dependencies):
    manager, _, _ = mock_dependencies
    
    # Simulate typing 'sandbox start' into the terminal
    mocker.patch("sys.argv", ["sandbox", "start"])
    main()
    
    manager.start.assert_called_once()

def test_cli_stop(mocker, mock_dependencies):
    manager, _, _ = mock_dependencies
    
    mocker.patch("sys.argv", ["sandbox", "stop"])
    main()
    
    manager.stop.assert_called_once()

def test_cli_remove(mocker, mock_dependencies):
    manager, _, _ = mock_dependencies
    
    mocker.patch("sys.argv", ["sandbox", "remove"])
    main()
    
    manager.remove.assert_called_once()

def test_cli_exec(mocker, mock_dependencies):
    """Verifies that the bash command string is rebuilt correctly from argparse nargs."""
    manager, _, _ = mock_dependencies
    
    mocker.patch("sys.argv", ["sandbox", "exec", "pwd && ls -la"])
    main()
    
    manager.exec_command.assert_called_once_with("pwd && ls -la")

def test_cli_monitor_default(mocker, mock_dependencies):
    manager, monitor_class, monitor_instance = mock_dependencies
    
    mocker.patch("sys.argv", ["sandbox", "monitor"])
    main()
    
    # Verify the monitor takes ownership of the manager and launches the UI with a 1.0s refresh
    monitor_class.assert_called_once_with(manager)
    monitor_instance.run.assert_called_once_with(1.0)

def test_cli_monitor_custom_refresh(mocker, mock_dependencies):
    manager, monitor_class, monitor_instance = mock_dependencies
    
    mocker.patch("sys.argv", ["sandbox", "monitor", "-r", "0.5"])
    main()
    
    monitor_instance.run.assert_called_once_with(0.5)

def test_cli_missing_command(mocker):
    """Verifies that the CLI correctly crashes and raises SystemExit if no command is given."""
    mocker.patch("sys.argv", ["sandbox"])
    with pytest.raises(SystemExit):
        main()
