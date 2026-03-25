import os
import time
import pytest
from unittest.mock import MagicMock
from flashbox.monitor import FlashboxMonitor
from flashbox.docker_manager import DockerManager

@pytest.fixture
def manager(mocker):
    # Mock manager to isolate monitor logic
    mgr = MagicMock(spec=DockerManager)
    mgr.cwd = "/fake/repo/path"
    mgr.container_name = "flashbox-fake-repo"
    mgr.is_running.return_value = True
    return mgr

@pytest.fixture
def monitor(manager):
    return FlashboxMonitor(manager)

def test_get_docker_stats_success(monitor, manager):
    """Verifies that the raw output from docker stats is parsed correctly."""
    manager._run_cmd.return_value = "5.50%|150MiB / 2GiB"
    cpu, mem = monitor._get_docker_stats()
    
    # Needs to match the docker stats command signature in the monitor
    manager._run_cmd.assert_called_once_with(
        f"docker stats --no-stream --format '{{{{.CPUPerc}}}}|{{{{.MemUsage}}}}' {manager.container_name}",
        check=False
    )
    assert cpu == "5.50%"
    assert mem == "150MiB / 2GiB"

def test_get_docker_stats_not_running(monitor, manager):
    manager.is_running.return_value = False
    cpu, mem = monitor._get_docker_stats()
    assert cpu == "N/A"
    assert mem == "N/A"

def test_get_docker_stats_error_handling(monitor, manager):
    """Verifies the monitor degrades gracefully if the docker daemon fails to return stats."""
    manager._run_cmd.side_effect = Exception("Docker daemon dead")
    cpu, mem = monitor._get_docker_stats()
    assert cpu == "Error"
    assert mem == "Error"

def test_format_size(monitor):
    """Verifies the iterative bytes to human readable formatting logic."""
    assert monitor._format_size(500) == "500.0 B"
    assert monitor._format_size(1024) == "1.0 KB"
    assert monitor._format_size(1024 * 1024 * 5) == "5.0 MB"
    assert monitor._format_size(1024 * 1024 * 1024 * 2.5) == "2.5 GB"

def test_get_sandbox_size_filtering_and_calculation(monitor, mocker):
    """
    Very important test: The sandbox scans the host volume to detect changes.
    It MUST skip .git and .venv folders, and properly evaluate file modification times.
    """
    # Mocking os.walk to return a fake file structure
    # Structure: 
    # /fake/repo/path/
    #   - file1.py (size 100)
    #   - .git/
    #       - obj1.pack (size 5000) -> SHOULD BE SKIPPED
    #   - .venv/
    #       - bin/python (size 2000) -> SHOULD BE SKIPPED
    #   - src/
    #       - file2.py (size 300)
    
    mock_walk = mocker.patch("os.walk")
    mock_walk.return_value = [
        ("/fake/repo/path", ("src", ".git", ".venv"), ("file1.py",)),
        ("/fake/repo/path/.git", (), ("obj1.pack",)),
        ("/fake/repo/path/.venv", ("bin",), ()),
        ("/fake/repo/path/.venv/bin", (), ("python",)),
        ("/fake/repo/path/src", (), ("file2.py",)),
    ]
    
    # Mock sizes
    def mock_getsize(path):
        sizes = {
            "/fake/repo/path/file1.py": 100,
            "/fake/repo/path/src/file2.py": 300,
            # We add these just to ensure they don't break if mistakenly called
            "/fake/repo/path/.git/obj1.pack": 5000,
            "/fake/repo/path/.venv/bin/python": 2000,
        }
        return sizes.get(path, 0)
    
    mocker.patch("os.path.getsize", side_effect=mock_getsize)
    mocker.patch("os.path.islink", return_value=False)
    
    # Mock the time so we can check activity tracking
    current_time = 1000.0
    mocker.patch("time.time", return_value=current_time)
    
    def mock_getmtime(path):
        # file1.py is old (idle)
        # file2.py is new (active, modified 5 seconds ago)
        times = {
            "/fake/repo/path/file1.py": current_time - 100,
            "/fake/repo/path/src/file2.py": current_time - 5,
        }
        return times.get(path, current_time - 100)
        
    mocker.patch("os.path.getmtime", side_effect=mock_getmtime)
    
    # Execute
    monitor._get_sandbox_size()
    
    # Asserts
    assert monitor.total_files == 2, "Should only count file1.py and file2.py, skipping .git and .venv"
    assert monitor.total_size == 400, "Should sum up size of file1.py and file2.py only"
    assert monitor.last_active_time == current_time, "Since file2 was recently edited, active time should be updated to check time"
