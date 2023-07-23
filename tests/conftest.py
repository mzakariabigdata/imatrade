"""Module to define fixtures for pytest."""

import os
import pytest

from imobject import ObjDict
from src.imatrade.utils.config import Config


from src.imatrade.controller.trading_indicators_controller import (
    TradingIndicatorsController,
)
from src.imatrade.factory.trading_indicators_factory import TradingIndicatorsFactory
from src.imatrade.controller.treading_data_controller import TreadingDataController
from src.imatrade.data_providers.oanda_data import OandaDataProvider

from src.imatrade.controller.trading_strategy_controller import (
    TradingStrategyController,
)
from src.imatrade.factory.trading_strategy_factory import TradingStrategyFactory
from src.imatrade.controller.trading_backtest_controller import (
    TradingBacktestController,
)
from src.imatrade.factory.trading_backtests_factory import TradingBacktestsFactory


@pytest.fixture()
def trading_backtest_controller():
    """Fixture to return hello world."""
    app_for_test = ObjDict()
    app_for_test.backtests_config = Config(
        os.path.join(os.path.dirname(__file__), "config", "backtests.yml")
    ).load_config()

    backtests_factory = TradingBacktestsFactory(
        app_for_test.backtests_config.backtests_composer
    )
    oanda_data_provider = OandaDataProvider(api_key=os.getenv("OANDA_API_KEY"))
    treading_data_controller = TreadingDataController(oanda_data_provider)
    trading_backtest_controller_fixture = TradingBacktestController(
        backtests_factory, treading_data_controller
    )

    return trading_backtest_controller_fixture


@pytest.fixture()
def trading_indicators_controller():
    """Fixture to return hello world."""
    app_for_test = ObjDict()
    app_for_test.indicators_config = Config(
        os.path.join(os.path.dirname(__file__), "config", "indicators.yml")
    ).load_config()

    indicators_factory = TradingIndicatorsFactory(
        app_for_test.indicators_config.indicators_composer
    )
    oanda_data_provider = OandaDataProvider(api_key=os.getenv("OANDA_API_KEY"))
    treading_data_controller = TreadingDataController(oanda_data_provider)
    trading_indicators_controller_fixture = TradingIndicatorsController(
        indicators_factory, treading_data_controller
    )

    return trading_indicators_controller_fixture


@pytest.fixture()
def trading_strategy_controller():
    """Fixture to return hello world."""

    app_for_test = ObjDict()
    app_for_test.strategies_config = Config(
        os.path.join(os.path.dirname(__file__), "config", "strategies.yml")
    ).load_config()

    strategy_factory = TradingStrategyFactory(
        app_for_test.strategies_config.strategies_composer
    )
    oanda_data_provider = OandaDataProvider(api_key=os.getenv("OANDA_API_KEY"))
    treading_data_controller = TreadingDataController(oanda_data_provider)
    trading_strategy_controller_fixture = TradingStrategyController(
        strategy_factory, treading_data_controller, None
    )
    return trading_strategy_controller_fixture
