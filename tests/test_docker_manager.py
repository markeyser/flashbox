import os
import sys
import pytest
from unittest.mock import MagicMock
from flashbox.docker_manager import DockerManager

@pytest.fixture
def mock_run_cmd(mocker):
    return mocker.patch("flashbox.docker_manager.DockerManager._run_cmd")

@pytest.fixture
def manager():
    # Use a fixed path to ensure consistent naming across OS
    return DockerManager(cwd="/Users/test/projects/My-Cool_App.1")

def test_generate_container_name_strips_invalid_chars(manager):
    """Verifies the container name strictly enforces docker character requirements."""
    name = manager._generate_container_name("/path/with/wierd/!@#$/Repo Name!")
    assert name == "flashbox-reponame", "Should strip spaces and special characters."

    name = manager._generate_container_name("/path/normal-repo.app_1")
    assert name == "flashbox-normal-repo.app_1", "Should retain dashes, dots, and underscores."

def test_is_running_true(manager, mock_run_cmd):
    """Tests the running check logic when container is active."""
    mock_run_cmd.return_value = "container_id_123"
    assert manager.is_running() is True
    mock_run_cmd.assert_called_once_with(f"docker ps -q -f name={manager.container_name}", check=False)

def test_is_running_false(manager, mock_run_cmd):
    """Tests the running check logic when container is absent."""
    mock_run_cmd.return_value = ""
    assert manager.is_running() is False

def test_start_already_running(manager, mock_run_cmd, mocker):
    """If the container is already running, start should exit early."""
    mocker.patch.object(manager, "is_running", return_value=True)
    manager.start()
    # It should not call any more docker commands
    mock_run_cmd.assert_not_called()

def test_start_existing_but_stopped(manager, mock_run_cmd, mocker):
    """If the container exists but is stopped, it should use docker start instead of run."""
    mocker.patch.object(manager, "is_running", return_value=False)
    # Mock 'docker ps -aq' returning an ID (container exists)
    mock_run_cmd.return_value = "container_id_123"
    
    manager.start()
    
    mock_run_cmd.assert_any_call(f"docker ps -aq -f name={manager.container_name}", check=False)
    mock_run_cmd.assert_called_with(f"docker start {manager.container_name}")
    # Ensure it doesn't trigger apt-get on existing containers
    assert mock_run_cmd.call_count == 2

def test_start_new_initialization(manager, mock_run_cmd, mocker):
    """If the container is missing entirely, it must perform the full run and tool initialization sequence."""
    mocker.patch.object(manager, "is_running", return_value=False)
    # Mock 'docker ps -aq' returning empty string (no container)
    mock_run_cmd.return_value = ""
    
    manager.start()
    
    # 1. ps -aq check
    # 2. docker run
    # 3. apt-get update
    # 4. apt-get install
    assert mock_run_cmd.call_count == 4
    
    # Check that volume mount points correctly to the init CWD
    call_args_str = str(mock_run_cmd.mock_calls[1])
    assert "docker run -d --name flashbox-my-cool_app.1" in call_args_str
    assert f"-v /Users/test/projects/My-Cool_App.1:/vault" in call_args_str
    
def test_stop(manager, mock_run_cmd, mocker):
    """Verify that stop properly checks state and executes the docker command."""
    mocker.patch.object(manager, "is_running", return_value=True)
    manager.stop()
    mock_run_cmd.assert_called_once_with(f"docker stop {manager.container_name}")

def test_exec_command_triggers_start(manager, mocker):
    """Verify that running exec explicitly triggers a start if the sandbox is stopped."""
    mock_start = mocker.patch.object(manager, "start")
    mocker.patch.object(manager, "is_running", return_value=False)
    
    # Mock the actual system call to prevent running real 'docker exec'
    mock_subprocess = mocker.patch("subprocess.run")
    mock_exit = mocker.patch("sys.exit")
    
    manager.exec_command("echo hello")
    
    mock_start.assert_called_once()
    mock_subprocess.assert_called_once()
