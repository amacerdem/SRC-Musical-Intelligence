"""Tests for MI configuration."""

from mi.core.config import MIConfig, MI_CONFIG


def test_default_config():
    config = MIConfig()
    assert config.sample_rate == 44_100
    assert config.hop_length == 256
    assert config.r3_dim == 49
    assert config.device == "cpu"


def test_frame_rate_property():
    config = MIConfig()
    assert abs(config.frame_rate - 172.265625) < 0.001


def test_custom_config():
    config = MIConfig(device="cuda")
    assert config.device == "cuda"


def test_list_coercion():
    config = MIConfig(r3_groups=["consonance", "energy"])
    assert isinstance(config.r3_groups, tuple)


def test_singleton():
    assert MI_CONFIG is not None
    assert MI_CONFIG.sample_rate == 44_100
